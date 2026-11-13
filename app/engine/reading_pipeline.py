"""
app/engine/reading_pipeline.py
==============================
Section 17 Shared Reading Pipeline & Resumable Report Job Runner:
  Input -> Calculate -> Analyse -> Consolidate -> Write -> Check -> Deliver

GOVERNING RULES:
- Shared by Reports and Charm AI (one deterministic code path).
- `Calculate`, `Analyse`, and `Consolidate` are 100% deterministic engine stages (zero LLM)
  reusing `indications_engine` and existing Layer 1 engines.
- `Write` is the ONLY LLM stage (Gemini `temperature=0`, structured JSON `sections[{fact_ids[], text}]`,
  parallelizable per section, cached by SHA-256 of `facts + question/section`).
  Receives ONLY the PII-free `ReadingPlan` (never DOB, name, email, or phone).
- `Check` runs `validate_llm_explanation` (Section 9). On timeout, error, or validation failure,
  immediately falls back to plain deterministic library text — never shows failing LLM output.
- Report jobs persist idempotent stage checkpoints (zero PII) and resume from `last_completed_stage`.
"""

import concurrent.futures
import hashlib
import json
import logging
import os
import time
import urllib.request
from datetime import date
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from app.engine.indication_validator import (
    ALLOWED_STAGE_LABELS,
    DEFAULT_FOOTER,
    HEALTH_SAFETY_LINE,
    REMEDY_EFFORT_LINE,
    assert_no_pii_in_llm_payload,
    detect_event_prediction_question,
    validate_llm_explanation,
    validate_stage_event,
)
from app.engine.indications_engine import (
    answer_charm_indication_or_care_question,
    compute_full_indications_bundle,
)

# Section 9 exact system instruction for Gemini `Write` stage
SECTION_9_SYSTEM_INSTRUCTION = (
    "You explain numerology results using only the supplied facts and approved lines. "
    "Show the numbers behind each statement. Use indicative language (may, can, tends to). "
    "Do not add any number, meaning, remedy, month, name, event or claim that is not supplied. "
    "Do not decide whether a planet is benefic or malefic; use the supplied link. "
    "Do not predict events. Do not use banned phrases. Do not claim accuracy, authenticity or verification. "
    "Cite fact_ids for every statement. If the facts cannot answer the question, say so and offer the nearest topic."
)

# Section 17.C fixed plain-language stage labels for Charm AI SSE
CHARM_STAGE_SEQUENCE: Tuple[Tuple[str, str], ...] = (
    ("reading_birth_date", "Reading your birth date"),
    ("mapping_loshu_grid", "Mapping your Lo Shu grid"),
    ("checking_cycles", "Checking your cycles"),
    ("putting_reading_together", "Putting your reading together"),
    ("writing_answer", "Writing your answer"),
)

# Section 17.B Report Job 5-step sequence & Dashboard progress lines
REPORT_JOB_STAGES: Tuple[str, ...] = (
    "calculate",
    "analyse",
    "consolidate",
    "write",
    "check_deliver",
)

REPORT_STAGE_DASHBOARD_LABELS: Dict[str, str] = {
    "queued": "Step 1 of 5: reading your birth date",
    "calculate": "Step 1 of 5: reading your birth date",
    "analyse": "Step 2 of 5: checking your grid and cycles",
    "consolidate": "Step 3 of 5: putting your reading together",
    "write": "Step 4 of 5: writing your reading",
    "check_deliver": "Step 5 of 5: preparing your PDF",
    "completed": "Ready to download",
}

REPORT_DELAYED_MESSAGE = (
    "This is taking a little longer than usual. Your report will appear here when it is ready."
)
CHARM_LONG_STAGE_NOTICE = "Still working on your reading."

# In-memory SHA-256 cache for `Write` outputs: key = sha256(plan_hash + "::" + section_or_question)
_WRITE_SECTION_CACHE: Dict[str, Dict[str, Any]] = {}


def clear_write_cache_for_tests() -> None:
    _WRITE_SECTION_CACHE.clear()


def compute_write_cache_key(plan_hash: str, question_or_section_id: str) -> str:
    raw = f"{plan_hash}::{question_or_section_id.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_pii_free_gemini_request(
    reading_plan: Dict[str, Any],
    *,
    section_id: str,
    question: str = "",
    approved_draft_lines: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Builds the exact Gemini structured JSON request (`temperature = 0`).
    Contains ONLY calculated facts, logic links, approved lines, and the question/section ID.
    NEVER contains DOB, name, email, or phone.
    """
    vc = reading_plan.get("validator_constraints", {})
    user_payload = {
        "section_id": section_id,
        "question": question,
        "entitlement_tier": reading_plan.get("entitlement_tier", "charm_free"),
        "has_tension": bool(reading_plan.get("has_tension")),
        "supplied_fact_ids": vc.get("supplied_fact_ids", []),
        "allowed_numbers": vc.get("allowed_numbers", []),
        "allowed_planets": vc.get("allowed_planets", []),
        "allowed_months": vc.get("allowed_months", []),
        "facts": reading_plan.get("facts", {}),
        "logic_links": reading_plan.get("logic_links", []),
        "approved_lines": approved_draft_lines or {},
        "footer": reading_plan.get("footer", DEFAULT_FOOTER),
        "output_contract": {
            "required_footer_exact": reading_plan.get("footer", DEFAULT_FOOTER),
            "rules": (
                "Return JSON with non-empty sections[{fact_ids, text}] and footer. "
                "Every fact_ids item MUST come from supplied_fact_ids. "
                "Every digit in text MUST appear in allowed_numbers. "
                "Every planet in text MUST correspond to allowed_planets. "
                "Every calendar month in text MUST appear in allowed_months. "
                "Do not mention gemstones, mantras, or manifestation on free/basic tiers. "
                "If has_tension is true, include a 'Growth edge:' sentence."
            ),
        },
    }
    return {
        "system_instruction": {"parts": [{"text": SECTION_9_SYSTEM_INSTRUCTION}]},
        "generationConfig": {
            "temperature": 0,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "sections": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "fact_ids": {"type": "ARRAY", "items": {"type": "STRING"}},
                                "text": {"type": "STRING"},
                            },
                            "required": ["fact_ids", "text"],
                        },
                    },
                    "footer": {"type": "STRING"},
                },
                "required": ["sections", "footer"],
            },
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": json.dumps(user_payload, ensure_ascii=False, sort_keys=True)}],
            }
        ],
    }


def _plain_library_fallback_for_card(card: Dict[str, Any]) -> str:
    """Renders deterministic plain library text when `Write` is disabled, slow, or rejected by `Check`."""
    parts = [
        f"Your numbers: {card.get('your_numbers', '')}",
        f"Why this shows: {card.get('why_this_shows', '')}",
        f"What it may indicate: {card.get('what_it_may_indicate', '')}",
    ]
    if card.get("growth_edge"):
        parts.append(f"Growth edge: {card['growth_edge']}")
    if card.get("be_mindful_of"):
        parts.append(f"Be mindful of: {card['be_mindful_of']}")
    steps = card.get("gentle_steps") or []
    if steps:
        parts.append("Gentle steps: " + " ".join(steps))
    if card.get("remedy_effort_line"):
        parts.append(card["remedy_effort_line"])
    if card.get("health_safety_line"):
        parts.append(card["health_safety_line"])
    parts.append(card.get("footer") or DEFAULT_FOOTER)
    return "\n".join(p for p in parts if p)


def _default_gemini_transport(request_body: Dict[str, Any], timeout_sec: float) -> Optional[Dict[str, Any]]:
    """Calls Gemini `temperature=0` only when live LLM is enabled and API key is configured."""
    if (os.getenv("NV_DISABLE_LIVE_LLM") or "").strip().lower() in {"1", "true", "yes"}:
        return None
    api_key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    if not api_key or not api_key.startswith("AIza"):
        return None
    model_id = (os.getenv("NV_EXPLANATION_MODEL") or "gemini-2.5-flash").strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(request_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        raw = json.loads(resp.read().decode("utf-8"))
    cand_text = (
        raw.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    )
    return cand_text if cand_text else None


def write_and_check_section(
    reading_plan: Dict[str, Any],
    *,
    section_id: str,
    fallback_text: str,
    approved_lines: Optional[Dict[str, Any]] = None,
    question: str = "",
    requires_health_safety_line: bool = False,
    requires_growth_edge: Optional[bool] = None,
    llm_callable: Optional[Callable[[Dict[str, Any], float], Optional[Dict[str, Any]]]] = None,
    deadline_sec: float = 6.0,
) -> Dict[str, Any]:
    """
    Executes `Write -> Check` for a single section or Charm AI answer:
    1. Checks SHA-256 `(plan_hash + question/section_id)` cache first.
    2. Builds PII-free Gemini payload and asserts zero PII keys/values.
    3. Invokes `llm_callable` (or default Gemini transport) within `deadline_sec`.
    4. Validates structured output via `validate_llm_explanation`.
    5. On ANY timeout, exception, or validator rejection -> returns `fallback_text`
       with `used_fallback = True` and `llm_rejected = True` (never emits unvalidated text).
    """
    plan_hash = reading_plan.get("plan_hash", "")
    cache_key = compute_write_cache_key(plan_hash, f"{section_id}::{question}")
    if cache_key in _WRITE_SECTION_CACHE:
        cached = dict(_WRITE_SECTION_CACHE[cache_key])
        cached["cache_hit"] = True
        return cached

    req_body = build_pii_free_gemini_request(
        reading_plan,
        section_id=section_id,
        question=question,
        approved_draft_lines=approved_lines,
    )
    pii_issues = assert_no_pii_in_llm_payload(req_body)
    if pii_issues:
        raise ValueError(f"PII guard blocked LLM payload: {pii_issues}")

    transport = llm_callable or _default_gemini_transport
    audit_logger = logging.getLogger("numeros.indication_validator")
    tier_label = str(reading_plan.get("entitlement_tier") or "unknown")
    try:
        llm_raw = transport(req_body, deadline_sec)
    except Exception as exc:
        err_code = f"write_error:{type(exc).__name__}"
        audit_logger.warning(
            "LLM write failed and fell back to library text: section_id=%s tier=%s plan_hash=%s error_code=%s credit_charged=0",
            section_id,
            tier_label,
            plan_hash[:12],
            err_code,
        )
        return {
            "section_id": section_id,
            "text": fallback_text,
            "used_fallback": True,
            "llm_rejected": True,
            "credit_chargeable": False,
            "cache_hit": False,
            "error_code": err_code,
            "violations": [str(exc)],
            "request_payload": req_body,
        }

    if llm_raw is None:
        res = {
            "section_id": section_id,
            "text": fallback_text,
            "used_fallback": True,
            "llm_rejected": False,
            "credit_chargeable": True,
            "cache_hit": False,
            "error_code": None,
            "violations": [],
            "request_payload": req_body,
        }
        _WRITE_SECTION_CACHE[cache_key] = dict(res)
        return res

    llm_json: Any = llm_raw
    if isinstance(llm_raw, str):
        try:
            llm_json = json.loads(llm_raw)
        except Exception:
            audit_logger.warning(
                "LLM non-JSON reply rejected and fell back to library text: section_id=%s tier=%s plan_hash=%s error_code=non_json_reply credit_charged=0",
                section_id,
                tier_label,
                plan_hash[:12],
            )
            return {
                "section_id": section_id,
                "text": fallback_text,
                "used_fallback": True,
                "llm_rejected": True,
                "credit_chargeable": False,
                "cache_hit": False,
                "error_code": "non_json_reply",
                "violations": ["non_json_llm_reply"],
                "request_payload": req_body,
            }

    vc = reading_plan["validator_constraints"]
    req_ge = reading_plan.get("has_tension", False) if requires_growth_edge is None else requires_growth_edge
    check_res = validate_llm_explanation(
        llm_json,
        supplied_fact_ids=set(vc["supplied_fact_ids"]),
        allowed_numbers=set(vc["allowed_numbers"]),
        allowed_planets={int(x) for x in vc["allowed_planets"]},
        allowed_months=set(vc["allowed_months"]),
        allowed_remedy_text_blob=vc["allowed_remedy_text_blob"],
        requires_health_safety_line=requires_health_safety_line,
        requires_growth_edge=req_ge,
        entitlement_tier=tier_label,
    )

    if not check_res["valid"]:
        audit_logger.warning(
            "LLM output rejected by validator and fell back to library text: section_id=%s tier=%s plan_hash=%s violations=%s credit_charged=0",
            section_id,
            tier_label,
            plan_hash[:12],
            check_res["violations"],
        )
        return {
            "section_id": section_id,
            "text": fallback_text,
            "used_fallback": True,
            "llm_rejected": True,
            "credit_chargeable": False,
            "cache_hit": False,
            "error_code": "validator_rejected",
            "violations": check_res["violations"],
            "request_payload": req_body,
        }

    out = {
        "section_id": section_id,
        "text": check_res["rendered_text"],
        "used_fallback": False,
        "llm_rejected": False,
        "credit_chargeable": True,
        "cache_hit": False,
        "error_code": None,
        "violations": [],
        "request_payload": req_body,
    }
    _WRITE_SECTION_CACHE[cache_key] = dict(out)
    return out


def run_charm_pipeline_with_stage_events(
    *,
    day: int,
    month: int,
    year: int,
    question: str,
    gender: Optional[str] = "male",
    calling_name: str = "",
    entitlement_tier: str = "charm_free",
    edition: str = "india",
    user_remedy_style: Optional[str] = None,
    fallback_composer_fn: Optional[Callable[[], Dict[str, Any]]] = None,
    llm_callable: Optional[Callable[[Dict[str, Any], float], Optional[Dict[str, Any]]]] = None,
    on_stage_event: Optional[Callable[[Dict[str, Any]], None]] = None,
    stage_hooks_for_test: Optional[Dict[str, Callable[[], None]]] = None,
    long_stage_threshold_ms: int = 10000,
    deadline_sec: float = 6.0,
    reference_date: Optional[date] = None,
) -> Dict[str, Any]:
    """
    Runs the shared 5-step Charm AI pipeline (`Input -> Calculate -> Analyse -> Consolidate -> Write -> Check -> Deliver`)
    and emits real, PII-free stage events ONLY when each stage starts and finishes.
    """
    events: List[Dict[str, Any]] = []
    dob_Variants = (
        f"{day:02d}-{month:02d}-{year:04d}",
        f"{year:04d}-{month:02d}-{day:02d}",
        f"{day:02d}/{month:02d}/{year:04d}",
    )

    def _emit(step_idx: int, stage_key: str, label: str, status: str, elapsed_ms: int) -> None:
        ev: Dict[str, Any] = {
            "stage": stage_key,
            "label": label,
            "status": status,
            "step_index": step_idx,
            "total_steps": len(CHARM_STAGE_SEQUENCE),
            "elapsed_ms": elapsed_ms,
        }
        if elapsed_ms >= long_stage_threshold_ms:
            ev["delayed_notice"] = CHARM_LONG_STAGE_NOTICE
        issues = validate_stage_event(ev, raw_dob_strings=dob_Variants, raw_name=calling_name)
        if issues:
            raise ValueError(f"Invalid stage event blocked: {issues}")
        events.append(ev)
        if on_stage_event:
            on_stage_event(ev)

    def _run_hook(stage_key: str) -> None:
        if stage_hooks_for_test and stage_key in stage_hooks_for_test:
            stage_hooks_for_test[stage_key]()

    # Immediate check for concrete event-prediction questions (0 credits used)
    refusal = detect_event_prediction_question(question)
    if refusal:
        t0 = time.perf_counter()
        _emit(1, CHARM_STAGE_SEQUENCE[0][0], CHARM_STAGE_SEQUENCE[0][1], "started", 0)
        _run_hook(CHARM_STAGE_SEQUENCE[0][0])
        el = int((time.perf_counter() - t0) * 1000)
        _emit(1, CHARM_STAGE_SEQUENCE[0][0], CHARM_STAGE_SEQUENCE[0][1], "completed", el)
        topic_k, refusal_msg = refusal
        return {
            "status": "REFUSED_PREDICTION",
            "credit_chargeable": False,
            "topic": topic_k,
            "headline": "Reflective Guidance Boundary",
            "validated_text": refusal_msg,
            "practical_next_steps": [
                "Ask what your numbers may indicate for communication, pacing or daily habits in this area."
            ],
            "follow_up_question": f"What do my numbers indicate for steady habits in {topic_k} this year?",
            "stage_events": events,
            "used_fallback": False,
            "llm_rejected": False,
        }

    # Stage 1: Reading your birth date
    s1_t0 = time.perf_counter()
    _emit(1, *CHARM_STAGE_SEQUENCE[0], "started", 0)
    _run_hook("reading_birth_date")
    req_aff = any(w in question.lower() for w in ("affirmation", "manifest", "manifestation", "intention"))
    s1_el = int((time.perf_counter() - s1_t0) * 1000)
    _emit(1, *CHARM_STAGE_SEQUENCE[0], "completed", s1_el)

    # Stage 2: Mapping your Lo Shu grid & Stage 3: Checking your cycles & Stage 4: Putting your reading together
    s2_t0 = time.perf_counter()
    _emit(2, *CHARM_STAGE_SEQUENCE[1], "started", 0)
    _run_hook("mapping_loshu_grid")
    bundle = compute_full_indications_bundle(
        day=day,
        month=month,
        year=year,
        gender=gender,
        calling_name=calling_name,
        edition=edition,
        tier=entitlement_tier,
        entitlement_tier=entitlement_tier,
        user_remedy_style=user_remedy_style,
        requested_affirmation_on_demand=req_aff,
        reference_date=reference_date,
    )
    s2_el = int((time.perf_counter() - s2_t0) * 1000)
    _emit(2, *CHARM_STAGE_SEQUENCE[1], "completed", s2_el)

    s3_t0 = time.perf_counter()
    _emit(3, *CHARM_STAGE_SEQUENCE[2], "started", 0)
    _run_hook("checking_cycles")
    care_or_aff = answer_charm_indication_or_care_question(question, bundle, edition=edition)
    s3_el = int((time.perf_counter() - s3_t0) * 1000)
    _emit(3, *CHARM_STAGE_SEQUENCE[2], "completed", s3_el)

    s4_t0 = time.perf_counter()
    _emit(4, *CHARM_STAGE_SEQUENCE[3], "started", 0)
    _run_hook("putting_reading_together")
    reading_plan = bundle["reading_plan"]
    if care_or_aff is not None:
        base_headline = care_or_aff["headline"]
        base_text = care_or_aff["text"]
        base_steps = care_or_aff["next_steps"]
        base_followup = care_or_aff["follow_up_question"]
        base_topic = care_or_aff["topic"]
        base_status = "ANSWERED"
    elif fallback_composer_fn is not None:
        composed = fallback_composer_fn()
        base_status = composed.get("status", "ANSWERED")
        base_topic = composed.get("topic", "general")
        base_headline = composed.get("human_friendly_summary", {}).get("headline", "Personal Guidance")
        base_text = composed.get("assistant_message", {}).get("text", "")
        base_steps = composed.get("practical_next_steps", [])
        base_followup = composed.get("follow_up_question", "")
    else:
        primary_card = bundle["indication_cards"][0] if bundle["indication_cards"] else {}
        base_status = "ANSWERED"
        base_topic = "general"
        base_headline = primary_card.get("title", "Personal Numerology Guidance")
        base_text = _plain_library_fallback_for_card(primary_card) if primary_card else DEFAULT_FOOTER
        base_steps = primary_card.get("gentle_steps", ["Keep one steady daily habit aligned with your priorities."])
        base_followup = "Which months should I take extra care in 2027?"
    s4_el = int((time.perf_counter() - s4_t0) * 1000)
    _emit(4, *CHARM_STAGE_SEQUENCE[3], "completed", s4_el)

    # Stage 5: Writing your answer (`Write` + `Check`)
    s5_t0 = time.perf_counter()
    _emit(5, *CHARM_STAGE_SEQUENCE[4], "started", 0)
    _run_hook("writing_answer")
    wc_res = write_and_check_section(
        reading_plan,
        section_id="charm_answer",
        fallback_text=base_text,
        approved_lines={"headline": base_headline, "library_text": base_text},
        question=question,
        requires_health_safety_line=(HEALTH_SAFETY_LINE in base_text),
        llm_callable=llm_callable,
        deadline_sec=deadline_sec,
    )
    s5_el = int((time.perf_counter() - s5_t0) * 1000)
    _emit(5, *CHARM_STAGE_SEQUENCE[4], "completed", s5_el)

    is_chargeable = (base_status == "ANSWERED" and not wc_res["llm_rejected"])
    return {
        "status": base_status,
        "credit_chargeable": is_chargeable,
        "credits_charged": 1 if is_chargeable else 0,
        "topic": base_topic,
        "headline": base_headline,
        "validated_text": wc_res["text"],
        "practical_next_steps": base_steps,
        "follow_up_question": base_followup,
        "stage_events": events,
        "used_fallback": wc_res["used_fallback"],
        "llm_rejected": wc_res["llm_rejected"],
        "error_code": wc_res["error_code"],
        "validator_violations": wc_res["violations"],
        "cache_hit": wc_res["cache_hit"],
        "reading_plan_hash": reading_plan["plan_hash"],
        "affirmation_and_manifestation": bundle["affirmation_and_manifestation"],
    }


def format_dashboard_progress_for_job(
    job_row: Dict[str, Any],
    *,
    now_ms: Optional[int] = None,
    delayed_after_ms: int = 45000,
) -> Dict[str, Any]:
    """
    Section 17.B Dashboard progress formatter from `report_jobs` row (zero PII):
    - Returns `"Step 3 of 5: putting your reading together"` etc.
    - When `now_ms - created_at > delayed_after_ms` and still preparing, includes
      `"This is taking a little longer than usual. Your report will appear here when it is ready."`
    """
    st = str(job_row.get("status") or "QUEUED").upper()
    cur_stage = str(job_row.get("current_stage") or "queued").lower()
    now_val = now_ms if now_ms is not None else int(time.time() * 1000)
    created_at = int(job_row.get("created_at") or now_val)
    elapsed_ms = max(0, now_val - created_at)

    if st in {"COMPLETED", "DOWNLOADED"}:
        return {
            "progress_line": "Ready to download",
            "delayed_notice": None,
            "is_delayed": False,
        }
    if st == "FAILED":
        return {
            "progress_line": "We’re checking this order.",
            "delayed_notice": None,
            "is_delayed": False,
        }

    progress_line = REPORT_STAGE_DASHBOARD_LABELS.get(
        cur_stage, "Step 1 of 5: reading your birth date"
    )
    is_delayed = elapsed_ms >= delayed_after_ms
    return {
        "progress_line": progress_line,
        "delayed_notice": REPORT_DELAYED_MESSAGE if is_delayed else None,
        "is_delayed": is_delayed,
    }


class ResumableReportJobRunner:
    """
    Section 17.B Idempotent, Resumable Report Pipeline Runner:
      Stages: `calculate -> analyse -> consolidate -> write -> check_deliver`
    - Stores strictly non-PII job rows (`job_id, order_id, tier, current_stage,
      last_completed_stage, stage_timestamps_json, status, attempts, error_code,
      reading_plan_hash, fallback_sections_count`).
    - Resumes from the stage immediately after `last_completed_stage` after any crash.
    - Parallelises `Write` across sections via `ThreadPoolExecutor` and falls back per section
      to plain library text if `Write` is slow or fails `Check`, so the report is NEVER incomplete.
    """

    def __init__(self, job_store: Optional[Dict[str, Dict[str, Any]]] = None):
        self.jobs: Dict[str, Dict[str, Any]] = job_store if job_store is not None else {}
        self._ephemeral_artifacts: Dict[str, Dict[str, Any]] = {}

    def create_job(self, *, job_id: str, order_id: str, tier: str, now_ms: Optional[int] = None) -> Dict[str, Any]:
        ts = now_ms if now_ms is not None else int(time.time() * 1000)
        row = {
            "id": job_id,
            "order_id": order_id,
            "tier": tier,
            "current_stage": "queued",
            "last_completed_stage": None,
            "stage_timestamps_json": "{}",
            "status": "QUEUED",
            "attempts": 0,
            "max_attempts": 3,
            "error_code": None,
            "reading_plan_hash": None,
            "fallback_sections_count": 0,
            "created_at": ts,
            "updated_at": ts,
            "completed_at": None,
        }
        self.jobs[job_id] = row
        return dict(row)

    def run_or_resume(
        self,
        job_id: str,
        *,
        day: int,
        month: int,
        year: int,
        gender: str = "male",
        edition: str = "india",
        llm_callable: Optional[Callable[[Dict[str, Any], float], Optional[Dict[str, Any]]]] = None,
        deliver_fn: Optional[Callable[[Dict[str, Any]], str]] = None,
        simulate_crash_at_stage: Optional[str] = None,
        stage_deadline_sec: float = 5.0,
    ) -> Dict[str, Any]:
        row = self.jobs[job_id]
        if row["status"] in {"COMPLETED", "DOWNLOADED"}:
            return dict(row)

        timestamps = json.loads(row.get("stage_timestamps_json") or "{}")
        last_done = row.get("last_completed_stage")
        start_idx = (REPORT_JOB_STAGES.index(last_done) + 1) if last_done in REPORT_JOB_STAGES else 0

        row["status"] = "PROCESSING"
        row["updated_at"] = int(time.time() * 1000)
        ctx = self._ephemeral_artifacts.setdefault(job_id, {})

        def _ensure_bundle() -> Dict[str, Any]:
            if "bundle" not in ctx:
                ctx["bundle"] = compute_full_indications_bundle(
                    day=day,
                    month=month,
                    year=year,
                    gender=gender,
                    edition=edition,
                    tier=row["tier"],
                    entitlement_tier=row["tier"],
                )
            return ctx["bundle"]

        try:
            for stage in REPORT_JOB_STAGES[start_idx:]:
                row["current_stage"] = stage
                st_start = int(time.time() * 1000)
                timestamps.setdefault(stage, {})["started_at"] = st_start
                row["stage_timestamps_json"] = json.dumps(timestamps)

                if simulate_crash_at_stage == stage:
                    raise RuntimeError(f"simulated_crash:{stage}")

                if stage == "calculate":
                    bundle = _ensure_bundle()
                    ctx["foundation_ready"] = True
                elif stage == "analyse":
                    bundle = _ensure_bundle()
                    ctx["links_count"] = len(bundle["reading_plan"]["logic_links"])
                elif stage == "consolidate":
                    bundle = _ensure_bundle()
                    row["reading_plan_hash"] = bundle["reading_plan"]["plan_hash"]
                elif stage == "write":
                    bundle = _ensure_bundle()
                    plan = bundle["reading_plan"]
                    cards = bundle["indication_cards"]
                    written_sections: List[Dict[str, Any]] = []
                    fallback_count = 0
                    if cards:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(cards))) as pool:
                            futures = [
                                pool.submit(
                                    write_and_check_section,
                                    plan,
                                    section_id=c["card_id"],
                                    fallback_text=_plain_library_fallback_for_card(c),
                                    approved_lines=c,
                                    llm_callable=llm_callable,
                                    deadline_sec=stage_deadline_sec,
                                )
                                for c in cards
                            ]
                            for fut in futures:
                                res = fut.result(timeout=stage_deadline_sec + 2.0)
                                if res["used_fallback"]:
                                    fallback_count += 1
                                written_sections.append(res)
                    ctx["written_sections"] = written_sections
                    row["fallback_sections_count"] = fallback_count
                elif stage == "check_deliver":
                    bundle = _ensure_bundle()
                    if deliver_fn is not None:
                        ctx["r2_key"] = deliver_fn(bundle)
                    else:
                        ctx["r2_key"] = f"reports/{row['tier']}/{job_id}.pdf"

                st_done = int(time.time() * 1000)
                timestamps[stage]["completed_at"] = st_done
                row["last_completed_stage"] = stage
                row["stage_timestamps_json"] = json.dumps(timestamps)
                row["updated_at"] = st_done

            row["current_stage"] = "completed"
            row["status"] = "COMPLETED"
            row["error_code"] = None
            row["completed_at"] = int(time.time() * 1000)
            return dict(row)

        except Exception as exc:
            row["attempts"] = int(row.get("attempts") or 0) + 1
            row["error_code"] = str(exc).split(":")[0][:64]
            row["status"] = "FAILED" if row["attempts"] >= row["max_attempts"] else "QUEUED"
            row["updated_at"] = int(time.time() * 1000)
            return dict(row)
