"""
app/engine/indication_validator.py
==================================
Deterministic language-rule, tone-rule, remedy-safety, named-person denylist,
PII-redaction, and Section 13/14 LLM explanation contract validators.
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

DEFAULT_FOOTER = "Numerology is a reflective guide, not a prediction."
HEALTH_SAFETY_LINE = "Traditional practice, in addition to medical care and sensible safety."
REMEDY_EFFORT_LINE = "These are choices you can make, and the effort is yours."
PHILOSOPHY_LINE = "Numbers are a guide, not a compulsion."

EVENT_REFUSAL_TEMPLATE_RELATIONSHIP = (
    "Numerology cannot say that. What I can explain is what your relationship numbers may indicate "
    "and how to look after that area. Would you like that?"
)

EVENT_REFUSAL_TEMPLATES_BY_TOPIC: Dict[str, str] = {
    "relationship": EVENT_REFUSAL_TEMPLATE_RELATIONSHIP,
    "safety": (
        "Numerology cannot say that. What I can explain is what your current cycle numbers may indicate "
        "for pacing and practical safety habits. Would you like that?"
    ),
    "health": (
        "Numerology cannot say that, and health questions belong with a qualified doctor. "
        "What I can explain is what your numbers may indicate for daily rest and steady routines. Would you like that?"
    ),
    "career": (
        "Numerology cannot say that. What I can explain is what your work and timing numbers may indicate "
        "and how to prepare steadily. Would you like that?"
    ),
    "money": (
        "Numerology cannot say that. What I can explain is what your numbers may indicate "
        "around financial structure and careful planning. Would you like that?"
    ),
    "legal": (
        "Numerology cannot say that. What I can explain is what your numbers may indicate "
        "around paperwork, patience and clear preparation. Would you like that?"
    ),
    "general": (
        "Numerology cannot say whether a specific event will happen. What I can explain is what your numbers "
        "may indicate and how to look after that area steadily. Would you like that?"
    ),
}

# Section 6 + Section 13.C + Section 14.A banned predictive, fear, guarantee & hype phrases
BANNED_INDICATION_PHRASES: Tuple[str, ...] = (
    "will happen",
    "guaranteed",
    "certain to",
    "is certain",
    "definitely",
    "destined",
    "cursed",
    "doomed",
    "protects you",
    "protect you from",
    "impact will reduce",
    "reduce the impact",
    "reduces the impact",
    "reduces impact",
    "diverts the event",
    "divert the event",
    "prevents the event",
    "prevent the event",
    "prevents accidents",
    "accident will happen",
    "you must",
    "the problem will come",
    "you will face",
    "you will suffer",
    "bad period",
    "unlucky",
    "this will pass because of the remedy",
    "pass because of the remedy",
    "will be solved",
    "problem will be solved",
    "solve your problem",
    "will fix",
    "fixes your",
    "fix your problem",
    "will heal",
    "heals the problem",
    "remove the problem",
    "removes the problem",
    "problem will be removed",
    "will be avoided",
    "problem will be avoided",
    "i am a human numerologist",
    "as a human numerologist",
    "the universe will bring",
    "universe guarantees",
    "manifest wealth instantly",
    "attract guaranteed money",
    "law of attraction guarantees",
    "wish will be granted",
    "will come true automatically",
)

# Standalone word boundaries for 'cure' and 'danger' so words like 'accurate'/'secure'/'endangered' are handled cleanly
BANNED_WORD_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    ("cure", re.compile(r"\bcures?\b", re.IGNORECASE)),
    ("danger", re.compile(r"\bdanger(?:ous)?\b", re.IGNORECASE)),
    ("accuracy_claim", re.compile(r"\b100%\s*accurate\b|\bscientifically\s+proven\b", re.IGNORECASE)),
    ("authenticity_claim", re.compile(r"\bverified\s+authentic\b|\bguaranteed\s+authentic\b", re.IGNORECASE)),
)

# Plain-language cleanup list across web UI / copy
BANNED_SITE_MARKETING_PHRASES: Tuple[str, ...] = (
    "verified numerological synthesis",
    "free calculation validated",
    "deterministic dossier selection",
    "sovereign pdf blueprint",
    "mathematical proofs",
    "execution windows",
    "deterministic mulank, bhagyank & kua calculations",
    "imperial premium sovereign dossier",
)

# Section 14.A harsh vocabulary replacements (order matters: multi-word first)
VOCABULARY_SOFTENING_MAP: Tuple[Tuple[re.Pattern, str], ...] = (
    (re.compile(r"\bescape\s+behaviou?r\b", re.IGNORECASE), "a wish to step back"),
    (re.compile(r"\bpower\s+abuse\b", re.IGNORECASE), "needs balance when holding authority"),
    (re.compile(r"\banger\b", re.IGNORECASE), "a short fuse under pressure"),
    (re.compile(r"\bgreed\b", re.IGNORECASE), "a pull toward control or status"),
    (re.compile(r"\barrogance\b", re.IGNORECASE), "a pull toward control or status"),
    (re.compile(r"\blaziness\b", re.IGNORECASE), "a tendency to delay"),
    (re.compile(r"\bprocrastination\b", re.IGNORECASE), "a tendency to delay"),
    (re.compile(r"\baccidents\b", re.IGNORECASE), "needs care with haste and safety"),
    (re.compile(r"\bweakness(?:es)?\s*:", re.IGNORECASE), "Growth edge:"),
    (re.compile(r"\bnegative\s*:", re.IGNORECASE), "Watch point:"),
)

HARSH_VOCABULARY_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    ("anger", re.compile(r"\banger\b", re.IGNORECASE)),
    ("greed", re.compile(r"\bgreed\b", re.IGNORECASE)),
    ("arrogance", re.compile(r"\barrogance\b", re.IGNORECASE)),
    ("laziness", re.compile(r"\blaziness\b", re.IGNORECASE)),
    ("procrastination", re.compile(r"\bprocrastination\b", re.IGNORECASE)),
    ("escape behaviour", re.compile(r"\bescape\s+behaviou?r\b", re.IGNORECASE)),
    ("accidents", re.compile(r"\baccidents\b", re.IGNORECASE)),
    ("power abuse", re.compile(r"\bpower\s+abuse\b", re.IGNORECASE)),
    ("weakness_label", re.compile(r"\bweakness(?:es)?\s*:", re.IGNORECASE)),
    ("negative_label", re.compile(r"\bnegative\s*:", re.IGNORECASE)),
)

# Section 5 prohibited remedy patterns
PROHIBITED_REMEDY_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    (
        "self_blood_or_injury",
        re.compile(
            r"\b(?:drop|draw|prick|spill|shed|offer)\b[^.]{0,40}\b(?:own\s+blood|your\s+blood|finger\s+blood)\b"
            r"|\bself[- ]?injur(?:y|e)\b|\bcut\s+yourself\b",
            re.IGNORECASE,
        ),
    ),
    (
        "hospital_water",
        re.compile(r"\bhospital\s+water\b|\bwater\s+from\s+(?:a\s+)?hospital\b|\bdrink[^.]{0,25}hospital\b", re.IGNORECASE),
    ),
    (
        "fasting_plan",
        re.compile(r"\bfasting\s+plan\b|\bkeep\s+a\s+fast\b|\bwaterless\s+fast\b|\bnirjala\b|\bstrict\s+fast(?:ing)?\b|\bupvas\b", re.IGNORECASE),
    ),
    (
        "stop_or_replace_medicine",
        re.compile(r"\b(?:stop|quit|replace|skip|discontinue)\s+(?:your\s+|taking\s+)?(?:medicine|medication|doctor|treatment)\b", re.IGNORECASE),
    ),
    (
        "paid_rituals_sold",
        re.compile(r"\b(?:buy|book|purchase|order)\s+(?:our\s+|a\s+)?(?:paid\s+)?(?:puja|pooja|ritual|havan|yagya)\b", re.IGNORECASE),
    ),
    (
        "gemstone_sales_push",
        re.compile(r"\b(?:buy|purchase|shop|order)\s+(?:this\s+|your\s+|certified\s+)?(?:gemstone|ruby|coral|sapphire|emerald|pearl|gomed|lehsunia)\b", re.IGNORECASE),
    ),
    (
        "river_dumping",
        re.compile(
            r"(?<!never )(?<!never litter or )\b(?:dump|throw|immerse|discard)\s+(?:offerings|coins|lead|coconuts|ash|items)\s+in\s+(?:a\s+|the\s+)?river",
            re.IGNORECASE,
        ),
    ),
    (
        "remedy_event_reduction_claim",
        re.compile(
            r"\bremed(?:y|ies)\s+(?:will\s+)?(?:prevent|divert|reduce|stop|cancel|avert)\b"
            r"|\b(?:prevents?|diverts?|averts?)\s+(?:an?\s+|the\s+)?(?:accident|illness|loss|divorce|event|misfortune)\b",
            re.IGNORECASE,
        ),
    ),
)

# Specific event-prediction patterns in outputs
EVENT_PREDICTION_OUTPUT_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    (
        "predicted_event",
        re.compile(
            r"\byou\s+will\s+(?:lose\b|get\s+divorced|divorce|have\s+an?\s+accident|fall\s+ill|die|win\s+the\s+case|pass\s+the\s+exam|fail\s+the\s+exam|conceive|get\s+pregnant)\b"
            r"|\b(?:divorce|accident|death|illness|bankruptcy|pregnancy)\s+is\s+(?:certain|guaranteed|going\s+to\s+happen|inevitable)\b",
            re.IGNORECASE,
        ),
    ),
)

# Event-prediction user question patterns -> topic key
EVENT_PREDICTION_QUESTION_PATTERNS: Tuple[Tuple[str, re.Pattern], ...] = (
    (
        "relationship",
        re.compile(
            r"\bwill\s+(?:i|we|my\s+spouse|my\s+husband|my\s+wife|my\s+partner)\s+(?:get\s+divorced|divorce|separate|break\s+up)\b"
            r"|\b(?:am\s+i\s+going\s+to|will\s+my\s+marriage)\s+(?:divorce|end|break)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "safety",
        re.compile(
            r"\bwill\s+(?:an?\s+accident\s+happen|i\s+have\s+an?\s+accident|i\s+get\s+injured|i\s+crash)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "health",
        re.compile(
            r"\b(?:when\s+will\s+i\s+die|will\s+i\s+die|will\s+i\s+get\s+(?:cancer|sick|ill|disease)|will\s+i\s+get\s+pregnant|boy\s+or\s+girl\s+baby|pregnancy\s+outcome)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "legal",
        re.compile(
            r"\bwill\s+i\s+(?:win|lose)\s+(?:the\s+|my\s+)?(?:court\s+case|lawsuit|legal\s+case|trial)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "career",
        re.compile(
            r"\bwill\s+i\s+(?:pass|fail|clear)\s+(?:the\s+|my\s+)?(?:exam|test|interview)\b"
            r"|\bwill\s+i\s+(?:get\s+fired|lose\s+my\s+job)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "money",
        re.compile(
            r"\bwill\s+i\s+(?:go\s+bankrupt|lose\s+all\s+my\s+money|win\s+the\s+lottery)\b",
            re.IGNORECASE,
        ),
    ),
)

ALL_MONTH_NAMES: Tuple[str, ...] = (
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
)

ALL_PLANET_NAMES: Dict[str, int] = {
    "sun": 1, "surya": 1,
    "moon": 2, "chandra": 2,
    "jupiter": 3, "guru": 3,
    "rahu": 4,
    "mercury": 5, "budh": 5,
    "venus": 6, "shukra": 6,
    "ketu": 7,
    "saturn": 8, "shani": 8,
    "mars": 9, "mangal": 9,
}

WATCHED_REMEDY_KEYWORDS: Tuple[str, ...] = (
    "hanuman chalisa",
    "red lentil",
    "red lentils",
    "ghee lamp",
    "blood bank",
    "blood donation",
    "donating blood",
    "hospital welfare",
    "mantra",
    "chalisa",
    "ruby",
    "manik",
    "pearl",
    "moti",
    "yellow sapphire",
    "pukhraj",
    "hessonite",
    "gomed",
    "emerald",
    "panna",
    "diamond",
    "zircon",
    "cat's eye",
    "lehsunia",
    "blue sapphire",
    "neelam",
    "red coral",
    "moonga",
    "amethyst",
    "citrine",
    "peridot",
    "moonstone",
    "garnet",
    "carnelian",
    "lapis",
    "rudraksha",
    "yantra",
    "kavach",
    "talisman",
    "kala dhaga",
    "black thread",
    "copper coin",
    "silver ring",
    "copper ring",
    "iron ring",
    "camphor",
    "cloves",
    "salt water under",
    "feed black crows",
    "feed crows",
    "feed ants",
    "feed fish",
)

UNAPPROVED_REMEDY_PRESCRIPTION_RE = re.compile(
    r"\b(?:wear\s+an?\s+[a-z\s]{2,25}?(?:ring|bracelet|pendant|stone|thread|amulet)"
    r"|chant\s+[a-z\s]{2,30}"
    r"|burn\s+[a-z\s]{2,25}"
    r"|keep\s+[a-z\s]{2,25}?\s+under\s+your\s+(?:pillow|bed)"
    r"|feed\s+[a-z\s]{2,25}?(?:crows|dogs|cows|ants|fish))\b",
    re.IGNORECASE,
)

LOWER_TIER_FORBIDDEN_GEMSTONE_TERMS: Tuple[str, ...] = (
    "gemstone",
    "ruby",
    "manik",
    "pearl",
    "moti",
    "yellow sapphire",
    "pukhraj",
    "hessonite",
    "gomed",
    "emerald",
    "panna",
    "diamond",
    "zircon",
    "cat's eye",
    "lehsunia",
    "blue sapphire",
    "neelam",
    "red coral",
    "moonga",
    "amethyst",
    "citrine",
    "peridot",
    "moonstone",
    "lapis",
)

LOWER_TIER_FORBIDDEN_MANTRA_TERMS: Tuple[str, ...] = (
    "mantra",
    "chalisa",
    "japa",
    "beej",
    "gayatri",
    "om namah",
    "om shanti",
    "om suryaya",
    "om som",
    "om gram",
    "om shram",
    "om bram",
    "om bum",
    "om dram",
    "om pram",
    "om kram",
)

LOWER_TIER_FORBIDDEN_MANIFESTATION_TERMS: Tuple[str, ...] = (
    "manifestation",
    "year manifestation",
    "quarterly focus",
    "quarterly intention",
    "monthly intention",
    "weekly action",
    "review prompt",
    "90-day manifestation",
)


def soften_shadow_text(text: str) -> str:
    """Applies Section 14.A vocabulary replacements to soften harsh shadow wording."""
    out = str(text or "")
    for pattern, replacement in VOCABULARY_SOFTENING_MAP:
        out = pattern.sub(replacement, out)
    return out


def detect_event_prediction_question(question: str) -> Optional[Tuple[str, str]]:
    """
    If `question` asks to predict a concrete life event (divorce, accident, illness/death,
    court verdict, exam pass/fail, pregnancy outcome), returns `(topic, refusal_message)`.
    Otherwise returns `None`.
    """
    q = str(question or "").strip()
    if not q:
        return None
    for topic, pattern in EVENT_PREDICTION_QUESTION_PATTERNS:
        if pattern.search(q):
            return topic, EVENT_REFUSAL_TEMPLATES_BY_TOPIC[topic]
    return None


def check_text_language_and_remedy_rules(
    text: str,
    *,
    check_harsh_vocab: bool = True,
    check_marketing_phrases: bool = True,
) -> List[str]:
    """
    Scans `text` against Section 5, 6, 13.C, and 14.A rules.
    Returns a list of violation codes (empty list = clean).
    """
    violations: List[str] = []
    raw = str(text or "")
    lowered = raw.lower()

    for phrase in BANNED_INDICATION_PHRASES:
        if phrase in lowered:
            violations.append(f"banned_phrase:{phrase}")

    for code, pat in BANNED_WORD_PATTERNS:
        if pat.search(raw):
            violations.append(f"banned_word:{code}")

    if check_marketing_phrases:
        for phrase in BANNED_SITE_MARKETING_PHRASES:
            if phrase in lowered:
                violations.append(f"banned_marketing:{phrase}")

    if check_harsh_vocab:
        for code, pat in HARSH_VOCABULARY_PATTERNS:
            if pat.search(raw):
                violations.append(f"harsh_vocabulary:{code}")

    for code, pat in PROHIBITED_REMEDY_PATTERNS:
        if pat.search(raw):
            violations.append(f"prohibited_remedy:{code}")

    for code, pat in EVENT_PREDICTION_OUTPUT_PATTERNS:
        if pat.search(raw):
            violations.append(f"event_prediction:{code}")

    # Blood donation without licensed blood bank + eligibility qualification
    if re.search(r"\b(?:donate\s+blood|blood\s+donation|donating\s+blood)\b", raw, re.IGNORECASE):
        if "blood bank" not in lowered or "eligible" not in lowered:
            violations.append("prohibited_remedy:unqualified_blood_donation")

    return violations


def extract_numbers_from_text(text: str) -> Set[str]:
    """Extracts all integer tokens from `text`."""
    return set(re.findall(r"\b\d+\b", str(text or "")))


def extract_planets_from_text(text: str) -> Set[int]:
    """Extracts planet numbers (1..9) mentioned by English or Sanskrit name in `text`."""
    found: Set[int] = set()
    raw = str(text or "")
    for name, num in ALL_PLANET_NAMES.items():
        if re.search(rf"\b{re.escape(name)}\b", raw, re.IGNORECASE):
            found.add(num)
    return found


def extract_months_from_text(text: str) -> Set[str]:
    """
    Extracts calendar month names mentioned in `text`.
    Note: 'may' is only treated as the calendar month when capitalized ('May') AND
    followed/preceded by month context or not used as the modal auxiliary verb ('may feel', 'may indicate').
    """
    found: Set[str] = set()
    raw = str(text or "")
    for m in ALL_MONTH_NAMES:
        if m == "may":
            # Match capitalized 'May' when not followed by a lowercase verb like 'May indicate' at sentence start,
            # or when preceded by 'in May', 'before May', 'for May', 'May 2027', 'May (', 'May is'.
            for match in re.finditer(r"\bMay\b", raw):
                start, end = match.span()
                after = raw[end : end + 20]
                before = raw[max(0, start - 15) : start]
                if re.search(r"\b(?:in|for|before|after|during|until|of)\s+$", before, re.IGNORECASE) or re.match(
                    r"\s*(?:20\d\d|is\b|\(|:|,|\.)", after
                ):
                    found.add("may")
        else:
            if re.search(rf"\b{m}\b", raw, re.IGNORECASE):
                found.add(m)
    return found


def validate_llm_explanation(
    llm_output: Dict[str, Any],
    *,
    supplied_fact_ids: Set[str],
    allowed_numbers: Set[str],
    allowed_planets: Set[int],
    allowed_months: Set[str],
    allowed_remedy_text_blob: str = "",
    requires_health_safety_line: bool = False,
    requires_growth_edge: bool = False,
    entitlement_tier: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Section 13.C + 14.A server-side validator for structured LLM explanations.
    Schema expected:
        {
            "sections": [{"fact_ids": ["..."], "text": "..."}],
            "footer": "..."   # or included in final section
        }
    Returns `{"valid": bool, "violations": List[str], "rendered_text": str}`.
    """
    violations: List[str] = []
    if not isinstance(llm_output, dict):
        return {"valid": False, "violations": ["invalid_json_type"], "rendered_text": ""}

    sections = llm_output.get("sections")
    if not isinstance(sections, list) or len(sections) == 0:
        return {"valid": False, "violations": ["missing_or_empty_sections"], "rendered_text": ""}

    combined_parts: List[str] = []
    for idx, sec in enumerate(sections):
        if not isinstance(sec, dict):
            violations.append(f"section_{idx}:not_object")
            continue
        fids = sec.get("fact_ids")
        sec_text = str(sec.get("text") or "").strip()
        if not sec_text:
            violations.append(f"section_{idx}:empty_text")
            continue
        if not isinstance(fids, list) or len(fids) == 0:
            violations.append(f"section_{idx}:missing_fact_ids")
        else:
            for fid in fids:
                if str(fid) not in supplied_fact_ids:
                    violations.append(f"section_{idx}:unknown_fact_id:{fid}")
        combined_parts.append(sec_text)

    footer = str(llm_output.get("footer") or "").strip()
    if footer:
        combined_parts.append(footer)

    full_text = " ".join(combined_parts).strip()

    # 1. Language, banned phrases, harsh words, event predictions, prohibited remedies
    violations.extend(check_text_language_and_remedy_rules(full_text))

    # 2. Every number in text must appear in allowed_numbers (plus harmless '1' in 'one'—digits only are checked)
    text_numbers = extract_numbers_from_text(full_text)
    for num in sorted(text_numbers):
        if num not in allowed_numbers:
            violations.append(f"unsupplied_number:{num}")

    # 3. Every planet mentioned must appear in allowed_planets
    text_planets = extract_planets_from_text(full_text)
    for pl in sorted(text_planets):
        if pl not in allowed_planets:
            violations.append(f"unsupplied_planet:{pl}")

    # 4. Every calendar month mentioned must appear in allowed_months
    text_months = extract_months_from_text(full_text)
    allowed_months_lower = {m.lower() for m in allowed_months}
    for m in sorted(text_months):
        if m not in allowed_months_lower:
            violations.append(f"invented_month:{m}")

    # 5. No remedy outside the supplied remedy pack
    remedy_blob_lower = str(allowed_remedy_text_blob or "").lower()
    full_lower = full_text.lower()
    for kw in WATCHED_REMEDY_KEYWORDS:
        if kw in full_lower and kw not in remedy_blob_lower:
            violations.append(f"unsupplied_remedy:{kw}")
    for m_rx in UNAPPROVED_REMEDY_PRESCRIPTION_RE.finditer(full_lower):
        phrase = m_rx.group(0).strip()
        if phrase and phrase not in remedy_blob_lower:
            violations.append(f"unsupplied_remedy:{phrase}")

    # 5b. Section 19 Server-Side Tier Entitlement Gate (reject higher-tier items leaked to lower tiers)
    if entitlement_tier:
        tier_norm = str(entitlement_tier).strip().lower()
        is_lower_tier = tier_norm in {"free", "basic", "report_basic", "charm_free"}
        is_mid_tier = tier_norm in {"advanced", "report_advanced", "report_master", "charm_paid"}
        if is_lower_tier:
            for g_term in LOWER_TIER_FORBIDDEN_GEMSTONE_TERMS:
                if g_term in full_lower:
                    violations.append(f"tier_entitlement_leak:gemstone_on_{tier_norm}:{g_term}")
            for m_term in LOWER_TIER_FORBIDDEN_MANTRA_TERMS:
                if m_term in full_lower:
                    violations.append(f"tier_entitlement_leak:mantra_on_{tier_norm}:{m_term}")
            for mf_term in LOWER_TIER_FORBIDDEN_MANIFESTATION_TERMS:
                if mf_term in full_lower:
                    violations.append(f"tier_entitlement_leak:manifestation_on_{tier_norm}:{mf_term}")
        elif is_mid_tier:
            for prem_only in ("monthly intention", "weekly action", "review prompt", "month-by-month care guide"):
                if prem_only in full_lower and prem_only not in remedy_blob_lower:
                    violations.append(f"tier_entitlement_leak:premium_item_on_{tier_norm}:{prem_only}")

    # 6. Footer checks
    if DEFAULT_FOOTER.lower() not in full_lower:
        violations.append("missing_default_footer")
    if requires_health_safety_line and HEALTH_SAFETY_LINE.lower() not in full_lower:
        violations.append("missing_health_safety_line")

    # 7. Section 14.A growth-edge check when tension exists
    if requires_growth_edge:
        tension_markers = (
            "growth edge",
            "watch point",
            "be mindful",
            "extra care",
            "tendency",
            "pull between",
            "pull in different directions",
            "may feel stronger",
            "stand out",
            "short fuse",
            "over-working",
            "overthink",
        )
        if not any(marker in full_lower for marker in tension_markers):
            violations.append("missing_growth_edge_for_tension_profile")

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "rendered_text": full_text,
    }


def assert_no_pii_in_llm_payload(
    payload: Any,
    *,
    raw_dob_strings: Iterable[str] = (),
    raw_name: str = "",
    raw_email: str = "",
    raw_phone: str = "",
) -> List[str]:
    """
    Section 13.B / 13.F guard: verifies the LLM request payload never contains
    DOB, name, email, or phone keys or values.
    Returns list of violations (empty = clean).
    """
    violations: List[str] = []
    forbidden_keys = {"dob", "date_of_birth", "birth_date", "name", "full_name", "user_name", "email", "phone", "mobile"}

    def _walk(node: Any, path: str = "$") -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                k_low = str(k).lower()
                if k_low in forbidden_keys:
                    violations.append(f"forbidden_key:{path}.{k}")
                _walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                _walk(item, f"{path}[{i}]")

    _walk(payload)
    serialized = json.dumps(payload, ensure_ascii=False)
    serialized_lower = serialized.lower()

    for dob_s in raw_dob_strings:
        clean_dob = str(dob_s or "").strip()
        if len(clean_dob) >= 6 and clean_dob.lower() in serialized_lower:
            violations.append(f"pii_dob_leak:{clean_dob}")

    for label, secret_val in (("name", raw_name), ("email", raw_email), ("phone", raw_phone)):
        clean_val = str(secret_val or "").strip()
        if len(clean_val) >= 3 and clean_val.lower() in serialized_lower:
            violations.append(f"pii_{label}_leak")

    return violations


ALLOWED_STAGE_LABELS: Tuple[str, ...] = (
    "Reading your birth date",
    "Mapping your Lo Shu grid",
    "Checking your cycles",
    "Putting your reading together",
    "Writing your answer",
)


def validate_stage_event(
    event: Dict[str, Any],
    *,
    raw_dob_strings: Iterable[str] = (),
    raw_name: str = "",
) -> List[str]:
    """
    Section 17.C validator for live progress SSE stage events:
    - Only `stage`, `label`, `status`, `step_index`, `total_steps`, `elapsed_ms` allowed (no PII, no reasoning/CoT).
    - Label must be plain language (never 'verified', 'authentic', 'deterministic', or internal framework names).
    """
    violations: List[str] = []
    allowed_keys = {"stage", "label", "status", "step_index", "total_steps", "elapsed_ms", "delayed_notice"}
    for k in event.keys():
        if k not in allowed_keys:
            violations.append(f"disallowed_stage_event_key:{k}")

    label = str(event.get("label") or "")
    label_low = label.lower()
    for banned_lbl in ("verified", "authentic", "validated", "deterministic", "nv think", "bnn", "chain of thought", "thinking"):
        if banned_lbl in label_low:
            violations.append(f"banned_stage_label_word:{banned_lbl}")

    if label and label not in ALLOWED_STAGE_LABELS:
        violations.append(f"unexpected_stage_label:{label}")

    violations.extend(
        assert_no_pii_in_llm_payload(
            event,
            raw_dob_strings=raw_dob_strings,
            raw_name=raw_name,
        )
    )
    return violations



def load_name_denylist(denylist_path: Optional[str] = None) -> Dict[str, Any]:
    """Loads `app/data/name_denylist.json` (or custom path supplied by owner)."""
    path = Path(denylist_path) if denylist_path else Path(__file__).resolve().parents[1] / "data" / "name_denylist.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def scan_text_for_named_persons(
    text: str,
    *,
    file_path: str = "",
    denylist_config: Optional[Dict[str, Any]] = None,
) -> List[str]:
    """Scans a string for any prohibited real/named person or corporate case-study name."""
    cfg = denylist_config or load_name_denylist()
    hits: List[str] = []
    raw = str(text or "")
    for name in cfg.get("denylist", []):
        pat = re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE)
        if pat.search(raw):
            hits.append(name)

    # Also guard statutory fiduciary name outside legal/governance files
    fiduciary = cfg.get("exempt_statutory_fiduciary_name", "")
    exempt_substrs = cfg.get("exempt_statutory_files_substr", [])
    if fiduciary and re.search(rf"\b{re.escape(fiduciary)}\b", raw, re.IGNORECASE):
        if not any(sub.lower() in str(file_path).lower() for sub in exempt_substrs):
            hits.append(f"{fiduciary} (outside statutory legal files)")
    return hits


def scan_repo_for_named_persons(
    repo_root: Optional[str] = None,
    denylist_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Scans site HTML/JS, Python engines/services, data JSON, docs, and fixtures
    to verify zero real/named persons or celebrity/corporate case studies appear.
    """
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    cfg = load_name_denylist(denylist_path)
    scan_dirs = [
        root / "app" / "data",
        root / "app" / "static",
        root / "app" / "engine",
        root / "app" / "services",
        root / "app" / "api",
        root / "app" / "charm",
    ]
    skip_files = {"name_denylist.json"}
    allowed_exts = {".json", ".html", ".js", ".py", ".md"}
    findings: List[Dict[str, Any]] = []

    for d in scan_dirs:
        if not d.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [dn for dn in dirnames if dn not in {"__pycache__", "node_modules", ".git", "brand"}]
            for fn in filenames:
                if fn in skip_files:
                    continue
                fp = Path(dirpath) / fn
                if fp.suffix.lower() not in allowed_exts:
                    continue
                try:
                    content = fp.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                hits = scan_text_for_named_persons(content, file_path=str(fp.relative_to(root)), denylist_config=cfg)
                if hits:
                    findings.append({"file": str(fp.relative_to(root)).replace("\\", "/"), "matches": hits})
    return findings
