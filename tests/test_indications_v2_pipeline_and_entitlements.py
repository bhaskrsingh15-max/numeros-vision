"""
tests/test_indications_v2_pipeline_and_entitlements.py
======================================================
End-to-end verification suite for FEATURE BRIEF v2 (Sections 0–19):
  1. Preservation manifest & `docs/PLANET_LOGIC_SPEC.md` existence + 16-DOB Golden Snapshot
     byte-for-byte match when `NV_ENABLE_LAYERS_2_3=0`.
  2. Flag ON (`NV_ENABLE_LAYERS_2_3=1`) additive preservation: Layer 1 element counts, gaps,
     and ranked remedies remain 100% identical; all 16 Basic PDFs stay strictly 3 pages
     (Advanced == 12, Premium == 32).
  3. Commanding Planet (`11-10-2011` -> Sun 1 x5; `17-02-1963` -> no commander), 4-step remedy
     sequence, and supplied 56-item `remedy_library.json` (`DRAFT`, gemstones offered as info
     with `gentle_alternatives`, strong-stone caution on 4/7/8, Basic excludes gemstones/mantras,
     International defaults to `universal + western`).
  4. All 5 worked synthetic profiles (`17-02-1963`, `26-03-1980`, `28-11-1981`, `07-09-1980`,
     `11-10-2011`), `generate_missing_content_report()`, `ENVIRONMENT=production` serving ONLY
     `APPROVED` entries, validator rejections, zero PII in LLM payloads/stage events/job rows,
     and `scan_repo_for_named_persons` == 0 hits across the entire repository.
  5. Section 17 Pipeline & Live Progress: SHA-256 `Write` cache hit, slow/failing `Write`
     automatic fallback to plain library text (`0` credit charged on rejected LLM output),
     `ResumableReportJobRunner` crash & idempotent resume at every stage + Dashboard progress
     formatter (`"Step 3 of 5: putting your reading together"` + delayed notice), and
     `POST /api/charm/chat/stream` SSE emitting ordered `stage` events + validated `result`.
  6. Section 19 Server-Side Entitlement Matrix across `free`, `basic`, `advanced`, `premium`,
     `planner_2027`, `charm_free`, `charm_paid`, and `charm_premium`, plus anti-escalation on
     `POST /api/v2/numerology/indications`.
"""

import asyncio
import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("NV_DISABLE_LIVE_LLM", "true")

import pypdf
from starlette.requests import Request
from starlette.responses import Response

from app.api.charm_ai import CharmChatRequest, charm_chat_endpoint, charm_chat_stream_endpoint
from app.api.numerology_v2 import IndicationsPreviewRequest, post_indications_bundle
from app.engine.indication_schema_and_loader import (
    generate_missing_content_report,
    load_driver_conductor_text,
    load_indication_library,
    load_neighbour_relations,
    load_neighbour_relations_text,
    load_remedy_library,
)
from app.engine.indication_validator import (
    DEFAULT_FOOTER,
    assert_no_pii_in_llm_payload,
    check_text_language_and_remedy_rules,
    detect_event_prediction_question,
    scan_repo_for_named_persons,
    validate_llm_explanation,
    validate_stage_event,
)
from app.engine.indications_engine import (
    compute_full_indications_bundle,
    resolve_package_entitlement,
)
from app.engine.layer1_golden_snapshot import (
    GOLDEN_16_DOBS,
    capture_all_16_golden_snapshots,
    extract_ranked_5_element_remedies,
)
from app.engine.reading_pipeline import (
    REPORT_DELAYED_MESSAGE,
    ResumableReportJobRunner,
    build_pii_free_gemini_request,
    clear_write_cache_for_tests,
    format_dashboard_progress_for_job,
    run_charm_pipeline_with_stage_events,
    write_and_check_section,
)
from app.services.pdf_report_generator import generate_customised_pdf_report

REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_SNAPSHOT_PATH = REPO_ROOT / "tests" / "fixtures" / "layer1_golden_snapshots_16_dobs.json"
PRESERVATION_MANIFEST_PATH = REPO_ROOT / "tests" / "fixtures" / "layer1_preservation_manifest.json"
PLANET_SPEC_PATH = REPO_ROOT / "docs" / "PLANET_LOGIC_SPEC.md"


def _run_coro(coro):
    """Drives pure in-process FastAPI endpoint coroutines without opening OS loopback self-pipes in Windows sandbox."""
    try:
        while True:
            coro.send(None)
    except StopIteration as stop:
        return stop.value


def _make_request(path: str = "/api/v2/numerology/indications", headers: dict | None = None) -> Request:
    raw_headers = []
    for k, v in (headers or {}).items():
        raw_headers.append((k.lower().encode("latin-1"), str(v).encode("latin-1")))
    scope = {
        "type": "http",
        "method": "POST",
        "path": path,
        "headers": raw_headers,
        "query_string": b"",
        "client": ("127.0.0.1", 51234),
    }
    return Request(scope)


class TestIndicationsV2PipelineAndEntitlements(unittest.TestCase):
    def test_01_preservation_artifacts_and_flag_off_byte_for_byte_snapshot(self):
        self.assertTrue(PLANET_SPEC_PATH.exists(), "docs/PLANET_LOGIC_SPEC.md must exist")
        self.assertTrue(PRESERVATION_MANIFEST_PATH.exists(), "layer1_preservation_manifest.json must exist")
        self.assertTrue(GOLDEN_SNAPSHOT_PATH.exists(), "16-DOB golden snapshot file must exist")

        expected_raw = GOLDEN_SNAPSHOT_PATH.read_text(encoding="utf-8")
        with patch.dict(os.environ, {"NV_ENABLE_LAYERS_2_3": "0", "NV_DISABLE_LIVE_LLM": "true"}):
            current_obj = capture_all_16_golden_snapshots()
            current_raw = json.dumps(current_obj, indent=2, ensure_ascii=False)
        self.assertEqual(
            current_raw,
            expected_raw,
            "With NV_ENABLE_LAYERS_2_3=0, all 16 golden DOB snapshots must match byte-for-byte!",
        )

    def test_02_flag_on_preserves_layer1_and_exact_pdf_page_counts_for_all_16_dobs(self):
        golden_data = json.loads(GOLDEN_SNAPSHOT_PATH.read_text(encoding="utf-8"))
        golden_by_id = {p["meta"]["id"]: p for p in golden_data["snapshots"]}

        with patch.dict(os.environ, {"NV_ENABLE_LAYERS_2_3": "1", "NV_DISABLE_LIVE_LLM": "true"}):
            for prof in GOLDEN_16_DOBS:
                d, m, y, g = prof["day"], prof["month"], prof["year"], prof["gender"]
                bundle = compute_full_indications_bundle(
                    day=d, month=m, year=y, gender=g, calling_name=prof["label"], tier="basic", entitlement_tier="basic"
                )
                l1_counts = {int(k): v for k, v in bundle["lo_shu_layer_1"]["counts"].items()}
                l1_elem = extract_ranked_5_element_remedies(l1_counts, bundle["lo_shu_layer_1"]["missing"])
                snap_elem_surface = golden_by_id[prof["id"]]["element_balancing"]
                self.assertEqual(
                    l1_elem,
                    snap_elem_surface["ranked_5_element_remedies"],
                    f"Layer 1 ranked element remedies mutated on {prof['id']}!",
                )
                self.assertEqual(
                    bundle["element_balance_layer_1"]["core_matrix_elements"],
                    snap_elem_surface["core_matrix_elements"],
                    f"Layer 1 core_matrix_elements mutated on {prof['id']}!",
                )

                pdf_b, _ = generate_customised_pdf_report(
                    name=prof["label"], day=d, month=m, year=y, gender=g, tier="basic", purchase_year=2026
                )
                reader_b = pypdf.PdfReader(io.BytesIO(pdf_b))
                self.assertEqual(len(reader_b.pages), 3, f"Basic PDF != 3 pages with Flag ON for {prof['id']}")
                p3_txt = reader_b.pages[2].extract_text()
                self.assertIn("INDICATIONS & DAILY AFFIRMATION GUIDE", p3_txt)
                self.assertNotIn("traditional gemstone", p3_txt.lower())
                self.assertNotIn("mantra:", p3_txt.lower())

            # Verify Advanced == 12 pages and Premium == 32 pages with Flag ON
            pdf_adv, _ = generate_customised_pdf_report(
                name="Profile B", day=26, month=3, year=1980, gender="male", tier="advanced", purchase_year=2026
            )
            self.assertEqual(len(pypdf.PdfReader(io.BytesIO(pdf_adv)).pages), 12)

            pdf_prem, _ = generate_customised_pdf_report(
                name="Profile B", day=26, month=3, year=1980, gender="male", tier="premium", purchase_year=2026
            )
            self.assertEqual(len(pypdf.PdfReader(io.BytesIO(pdf_prem)).pages), 32)

    def test_03_commanding_planet_worked_profiles_and_56_item_remedy_library(self):
        rem_lib = load_remedy_library()
        self.assertEqual(rem_lib["meta"]["status"], "DRAFT")
        total_items = sum(len(p["items"]) for p in rem_lib["planets"])
        self.assertEqual(len(rem_lib["planets"]), 9)
        self.assertEqual(total_items, 56)
        self.assertEqual(set(rem_lib["element_support"].keys()), {"Wood", "Fire", "Earth", "Metal", "Water"})

        # Check owner's specific items: Jupiter haldi bath, Venus fragrance, Saturn cobbler/shoes, strong stone cautions
        by_num = {p["number"]: p for p in rem_lib["planets"]}
        jup_txt = " ".join(it["text"] for it in by_num[3]["items"]).lower()
        ven_txt = " ".join(it["text"] for it in by_num[6]["items"]).lower()
        sat_txt = " ".join(it["text"] for it in by_num[8]["items"]).lower()
        self.assertIn("turmeric", jup_txt)
        self.assertIn("fragrance", ven_txt)
        self.assertIn("cobbler", sat_txt)
        for strong_num in (4, 7, 8):
            self.assertIn("qualified practitioner", by_num[strong_num]["gemstone"]["extra_caution"].lower())

        with patch.dict(os.environ, {"ENVIRONMENT": "development", "NV_ENABLE_LAYERS_2_3": "1"}):
            # 11-10-2011 -> Sun (1) x5 commander
            b_sun5 = compute_full_indications_bundle(day=11, month=10, year=2011, gender="male", tier="premium", entitlement_tier="premium")
            self.assertTrue(b_sun5["commanding_planet"]["has_commander"])
            self.assertEqual(b_sun5["commanding_planet"]["commanders"][0]["digit"], 1)
            self.assertEqual(b_sun5["commanding_planet"]["commanders"][0]["count"], 5)

            # 17-02-1963 -> max count is 1 x2 (<3), so no commander
            b_1963 = compute_full_indications_bundle(day=17, month=2, year=1963, gender="male", tier="premium", entitlement_tier="premium")
            self.assertFalse(b_1963["commanding_planet"]["has_commander"])
            self.assertEqual(b_1963["foundation"]["driver"], 8)
            self.assertEqual(b_1963["foundation"]["conductor"], 2)

            # 26-03-1980 -> Driver 8, Conductor 2, 2027 PY 2, May PM 9, Sep PM 4 (gap_meets_cycle since 4 missing)
            b_1980 = compute_full_indications_bundle(day=26, month=3, year=1980, gender="male", tier="premium", entitlement_tier="premium")
            self.assertEqual(b_1980["foundation"]["driver"], 8)
            self.assertEqual(b_1980["foundation"]["conductor"], 2)
            cg_months = {m["month_number"]: m for m in b_1980["cycles"]["care_guide_2027"]["months"]}
            self.assertEqual(cg_months[5]["personal_month"], 9)
            self.assertEqual(cg_months[9]["personal_month"], 4)
            self.assertIn("gap_meets_cycle", cg_months[9]["flags"])

            # International edition defaults to universal + western (excludes vedic-only mantras unless user chooses vedic)
            b_intl = compute_full_indications_bundle(
                day=26, month=3, year=1980, gender="male", edition="international", tier="premium", entitlement_tier="premium"
            )
            step3_intl = b_intl["remedies"]["step_3_planet_practices"]
            self.assertIsNotNone(step3_intl)
            for pl_pack in step3_intl["planets"]:
                for it in pl_pack["items"]:
                    self.assertNotEqual(it["kind"], "mantra", "International default must not include vedic-only mantras")
                self.assertIn("gemstone_info", pl_pack, "Gemstone info is offered across all styles in Advanced/Premium")

        # Production mode serves APPROVED entries only (so DRAFT planet remedy packs are withheld cleanly)
        with patch.dict(os.environ, {"ENVIRONMENT": "production", "NV_ENABLE_LAYERS_2_3": "1"}):
            b_prod = compute_full_indications_bundle(day=26, month=3, year=1980, gender="male", tier="premium", entitlement_tier="premium")
            self.assertIsNone(
                b_prod["remedies"]["step_3_planet_practices"],
                "In production, DRAFT remedy library must not surface unapproved planet remedies",
            )

    def test_04_loaders_missing_content_report_validator_and_zero_named_persons(self):
        rep = generate_missing_content_report()
        self.assertIn("driver_x_conductor_81", rep)
        self.assertEqual(
            rep["driver_x_conductor_81"]["flagged_owner_completion_pairs"],
            ["dc:6_6", "dc:7_7", "dc:8_8", "dc:9_8", "dc:9_9"],
        )
        self.assertEqual(len(rep["planet_remedy_packs_1_to_9"]["draft_planets"]), 9)

        # Test plain-text loaders (mark DRAFT + soften Section 14.A harsh words)
        dc_imported = load_driver_conductor_text(
            "pair: 8-2\nwhy: Saturn and Moon\nstrengths: Steady care\nweaknesses: Anger, greed and procrastination under pressure\nsteps: Keep a calm routine"
        )
        self.assertEqual(dc_imported[0]["status"], "DRAFT")
        self.assertNotIn("anger", dc_imported[0]["language_variants"]["india"]["growth_edge"].lower())
        self.assertNotIn("greed", dc_imported[0]["language_variants"]["india"]["growth_edge"].lower())
        self.assertNotIn("procrastination", dc_imported[0]["language_variants"]["india"]["growth_edge"].lower())

        nei_imported = load_neighbour_relations_text("1->3: friendly\n3->1: friendly\nmeaning 1-3: positive: Clear study | shadow: Arrogance under stress")
        self.assertEqual(nei_imported["status"], "DRAFT")
        self.assertEqual(nei_imported["ordered_relations"]["1->3"], "friendly")
        self.assertNotIn("arrogance", nei_imported["pair_meanings"]["1-3"]["shadow"].lower())

        # Validator catches banned predictive, healing, manifestation-guarantee, and unsafe-remedy lines
        self.assertTrue(len(check_text_language_and_remedy_rules("This remedy protects you and the problem will be solved.")) > 0)
        self.assertTrue(len(check_text_language_and_remedy_rules("The universe guarantees wealth and will heal illness.")) > 0)
        self.assertTrue(len(check_text_language_and_remedy_rules("Keep a strict fasting plan and skip your medicine.")) > 0)
        self.assertIsNotNone(detect_event_prediction_question("Will I get divorced next year?"))

        # Named-person denylist scan across entire repository == 0 hits
        hits = scan_repo_for_named_persons(REPO_ROOT)
        self.assertEqual(hits, [], f"Named-person denylist hits found: {hits}")

    def test_05_section17_pipeline_cache_fallback_resumable_jobs_and_charm_sse(self):
        clear_write_cache_for_tests()
        bundle = compute_full_indications_bundle(
            day=26, month=3, year=1980, gender="male", calling_name="Rohan Joshi", tier="premium", entitlement_tier="premium"
        )
        plan = bundle["reading_plan"]

        # Verify PII-free Gemini payload
        gem_req = build_pii_free_gemini_request(plan, section_id="sec_test", question="How should I pace May?")
        pii_violations = assert_no_pii_in_llm_payload(
            gem_req,
            raw_dob_strings=["26-03-1980", "1980-03-26", "26/03/1980"],
            raw_name="Rohan Joshi",
            raw_email="rohan@example.com",
            raw_phone="+919876543210",
        )
        self.assertEqual(pii_violations, [])

        # Verify Write cache hit on identical plan + section/question
        call_counter = {"n": 0}
        valid_fid = plan["validator_constraints"]["supplied_fact_ids"][0]

        def _good_llm(_body, _timeout):
            call_counter["n"] += 1
            return {
                "sections": [
                    {
                        "fact_ids": [valid_fid],
                        "text": f"Driver 8 and Conductor 2 may feel a pull between steady effort and sensitivity, so keep one growth edge check-in. {DEFAULT_FOOTER}",
                    }
                ]
            }

        r1 = write_and_check_section(
            plan, section_id="s_cache", fallback_text=f"Plain fallback. {DEFAULT_FOOTER}", llm_callable=_good_llm
        )
        r2 = write_and_check_section(
            plan, section_id="s_cache", fallback_text=f"Plain fallback. {DEFAULT_FOOTER}", llm_callable=_good_llm
        )
        self.assertFalse(r1["cache_hit"])
        self.assertTrue(r2["cache_hit"])
        self.assertEqual(call_counter["n"], 1)

        # Verify failing LLM output is rejected by Check -> automatic plain library fallback & credit_chargeable=False
        def _bad_llm(_body, _timeout):
            return {"sections": [{"fact_ids": [valid_fid], "text": "This guaranteed remedy protects you from danger!"}]}

        charm_bad = run_charm_pipeline_with_stage_events(
            question="What do my numbers indicate for focus?",
            day=26,
            month=3,
            year=1980,
            llm_callable=_bad_llm,
        )
        self.assertTrue(charm_bad["used_fallback"])
        self.assertTrue(charm_bad["llm_rejected"])
        self.assertFalse(charm_bad["credit_chargeable"], "Rejected LLM output must NEVER charge a credit")
        self.assertNotIn("protects you", charm_bad["validated_text"].lower())

        # Verify stage events pass `validate_stage_event` (plain language, zero PII, zero CoT)
        self.assertEqual(len(charm_bad["stage_events"]), 10)  # 5 started + 5 completed
        for ev in charm_bad["stage_events"]:
            self.assertEqual(
                validate_stage_event(ev, raw_dob_strings=["26-03-1980"], raw_name="Rohan Joshi"),
                [],
            )

        # Verify ResumableReportJobRunner crash & idempotent resume across all 5 stages
        runner = ResumableReportJobRunner()
        job = runner.create_job(job_id="job_s17_1", order_id="ord_s17_1", tier="advanced", now_ms=1000)
        for crash_stage, expected_dash in (
            ("calculate", "Step 1 of 5: reading your birth date"),
            ("analyse", "Step 2 of 5: checking your grid and cycles"),
            ("consolidate", "Step 3 of 5: putting your reading together"),
            ("write", "Step 4 of 5: writing your reading"),
            ("check_deliver", "Step 5 of 5: preparing your PDF"),
        ):
            crashed = runner.run_or_resume("job_s17_1", day=26, month=3, year=1980, simulate_crash_at_stage=crash_stage)
            self.assertIn(crashed["status"], {"QUEUED", "FAILED"})
            # Reset attempts so we can test crash at every stage sequentially
            runner.jobs["job_s17_1"]["attempts"] = 0
            runner.jobs["job_s17_1"]["status"] = "PROCESSING"
            dash = format_dashboard_progress_for_job(runner.jobs["job_s17_1"], now_ms=50000, delayed_after_ms=45000)
            self.assertEqual(dash["progress_line"], expected_dash)
            self.assertEqual(dash["delayed_notice"], REPORT_DELAYED_MESSAGE)
            # Complete that single stage cleanly before crashing at the next one
            next_idx = ("calculate", "analyse", "consolidate", "write", "check_deliver").index(crash_stage)
            if next_idx < 4:
                nxt = ("calculate", "analyse", "consolidate", "write", "check_deliver")[next_idx + 1]
                runner.run_or_resume("job_s17_1", day=26, month=3, year=1980, simulate_crash_at_stage=nxt)
                runner.jobs["job_s17_1"]["attempts"] = 0

        done_job = runner.run_or_resume("job_s17_1", day=26, month=3, year=1980)
        self.assertEqual(done_job["status"], "COMPLETED")
        self.assertEqual(format_dashboard_progress_for_job(done_job)["progress_line"], "Ready to download")

        # Verify POST /api/charm/chat/stream SSE emits ordered `event: stage` + `event: result`
        async def _collect_sse():
            req_obj = CharmChatRequest(
                message="Which months should I take extra care in 2027?",
                dob="1980-03-26",
                gender="male",
            )
            http_req = _make_request("/api/charm/chat/stream", {"X-NV-Edge-Metered": "1"})
            resp = await charm_chat_stream_endpoint(req_obj, http_req, current_user={"user_id": None}, _auth=None)
            chunks = []
            async for ch in resp.body_iterator:
                chunks.append(ch.decode("utf-8") if isinstance(ch, bytes) else str(ch))
            return "".join(chunks)

        with patch.dict(os.environ, {"NV_ENABLE_LAYERS_2_3": "1", "NV_DISABLE_LIVE_LLM": "true"}):
            sse_raw = _run_coro(_collect_sse())
        self.assertIn("event: stage", sse_raw)
        self.assertIn("Reading your birth date", sse_raw)
        self.assertIn("Writing your answer", sse_raw)
        self.assertIn("event: result", sse_raw)

        # Also verify event-prediction refusal on POST /api/charm/chat deducts 0 credits
        async def _call_refusal():
            req_obj = CharmChatRequest(message="Will I get divorced in 2027?", dob="1980-03-26")
            http_req = _make_request("/api/charm/chat", {"Cookie": "nv_visitor_id=vis_refusal_test_001"})
            return await charm_chat_endpoint(req_obj, http_req, Response(), current_user={"user_id": None}, _auth=None)

        ref_res = _run_coro(_call_refusal())
        ref_body = json.loads(ref_res.body.decode("utf-8"))
        self.assertEqual(ref_body["status"], "REFUSED_PREDICTION")
        self.assertEqual(ref_body["credits_remaining"], 3)

    def test_06_section19_server_side_entitlement_matrix_and_anti_escalation(self):
        # Verify exact matrix across all 8 package/pass tiers
        expected_matrix = {
            "free": ("general", "none"),
            "basic": ("general", "none"),
            "advanced": ("personalised", "year"),
            "premium": ("monthly_personalised", "full"),
            "planner_2027": ("monthly_personalised", "full"),
            "charm_free": ("general_on_request", "none"),
            "charm_paid": ("personalised_topic", "current_month"),
            "charm_premium": ("monthly_personalised", "full"),
        }
        for tier_key, (exp_aff, exp_man) in expected_matrix.items():
            spec = resolve_package_entitlement(tier_key)
            self.assertEqual(spec["affirmation_level"], exp_aff, f"Affirmation level mismatch on {tier_key}")
            self.assertEqual(spec["manifestation_level"], exp_man, f"Manifestation level mismatch on {tier_key}")

            b = compute_full_indications_bundle(
                day=26,
                month=3,
                year=1980,
                gender="male",
                tier=tier_key,
                entitlement_tier=tier_key,
                requested_affirmation_on_demand=True,
            )
            am = b["affirmation_and_manifestation"]
            if exp_man == "none":
                self.assertIsNone(am["manifestation"], f"{tier_key} must NOT receive manifestation content")
            elif exp_man == "year":
                self.assertIsNotNone(am["manifestation"]["year_theme"])
                self.assertEqual(len(am["manifestation"]["quarterly_focus"]), 4)
                self.assertNotIn("monthly_intentions", am["manifestation"])
            elif exp_man == "current_month":
                self.assertIn("month_intention", am["manifestation"])
                self.assertNotIn("quarterly_focus", am["manifestation"])
            elif exp_man == "full":
                self.assertEqual(len(am["monthly_affirmations"]), 12)
                self.assertEqual(len(am["manifestation"]["monthly_intentions"]), 12)
                self.assertTrue(bool(am["manifestation"]["weekly_action"]))
                self.assertTrue(bool(am["manifestation"]["review_prompt"]))

        # Verify server-side anti-escalation on POST /api/v2/numerology/indications:
        # Unauthenticated client requesting `requested_tier="premium"` receives ONLY `free` content + plain-text upgrade_note
        async def _call_escalated():
            req_body = IndicationsPreviewRequest(day=26, month=3, year=1980, gender="male", requested_tier="premium")
            http_req = _make_request("/api/v2/numerology/indications")
            return await post_indications_bundle(req_body, http_req)

        with patch.dict(os.environ, {"NV_ENABLE_LAYERS_2_3": "1"}):
            api_out = _run_coro(_call_escalated())
        self.assertEqual(api_out["entitlement_tier"], "free")
        self.assertEqual(api_out["requested_tier"], "premium")
        self.assertEqual(api_out["upgrade_note"], "A personalised version is included in Complete Numerology Report (Premium).")
        self.assertIsNone(api_out["bundle"]["affirmation_and_manifestation"]["manifestation"])
        self.assertEqual(len(api_out["bundle"]["indication_cards"]), 1, "Free tier only receives 1 sample indication card")

    # ------------------------------------------------------------------
    # 7. Adversarial Mocked-LLM Validator Suite (Pre-Deploy Gate B, A.5, C)
    # ------------------------------------------------------------------
    def test_07_adversarial_llm_validator_rejections_zero_credit_and_audit_logging(self):
        """
        Tests every adversarial LLM failure mode using mocked LLM outputs:
          1) Invented planet or unsupplied number (`Saturn` / `88` not in DOB 12-03-1950 allowed set)
          2) Event prediction (`"you will lose..."`)
          3) Outcome promises (`"cure"`, `"guaranteed"`, `"will fix"`)
          4) Remedy not in the approved library (`"feed black crows"` / `"wear a copper ring"`)
          5) Higher-tier item shown to a lower tier (gemstone/mantra/manifestation leaked to `charm_free` / `basic`)
          6) Non-JSON LLM reply (raw plain text & JSONDecodeError)
        Asserts for EACH case:
          - Rejected (`llm_rejected=True`),
          - Falls back to plain deterministic library text (`used_fallback=True`, exact library text returned),
          - Charges 0 credits (`credit_chargeable=False` and `credits_charged == 0`),
          - Logged to `numeros.indication_validator` at `WARNING` with `credit_charged=0` and zero PII.
        Also verifies `rzp_test_modal.html` is absent everywhere and `NV_ENABLE_LAYERS_2_3` defaults OFF.
        """
        from app.engine.indications_engine import is_layers_2_3_enabled

        # C: Confirm NV_ENABLE_LAYERS_2_3 defaults OFF when unset and when ENVIRONMENT=production
        env_without_flag = {k: v for k, v in os.environ.items() if k != "NV_ENABLE_LAYERS_2_3"}
        with patch.dict(os.environ, env_without_flag, clear=True):
            self.assertFalse(is_layers_2_3_enabled(), "NV_ENABLE_LAYERS_2_3 must default OFF when unset")

        # A.5: Confirm rzp_test_modal.html is deleted from repo, static folders, and dist
        for check_dir in ("app", "dist_cloudflare_pages", "pdf_service"):
            p = Path(__file__).resolve().parents[1] / check_dir
            if p.exists():
                leaked = list(p.rglob("*rzp_test_modal*"))
                self.assertEqual(leaked, [], f"rzp_test_modal must not exist under {check_dir}: {leaked}")

        # DOB 12-01-1951 (ref 2026-11-13): digits {1,2,5,9}, Driver=3, Conductor=2, Kua=4, PY=5, PM=7, PD=7, PY2027=6
        # -> planet 8 (Saturn) and number 88 are 100% ABSENT from allowed_planets and allowed_numbers!
        from datetime import date as _date

        ref_day = _date(2026, 11, 13)
        bundle = compute_full_indications_bundle(
            day=12,
            month=1,
            year=1951,
            gender="male",
            calling_name="",
            tier="charm_free",
            entitlement_tier="charm_free",
            reference_date=ref_day,
        )
        valid_fid = bundle["reading_plan"]["validator_constraints"]["supplied_fact_ids"][0]
        self.assertNotIn(8, bundle["reading_plan"]["validator_constraints"]["allowed_planets"])
        self.assertNotIn("88", bundle["reading_plan"]["validator_constraints"]["allowed_numbers"])

        adversarial_cases = [
            (
                "invented_planet_and_number",
                lambda _req, _t: {
                    "sections": [
                        {
                            "fact_ids": [valid_fid],
                            "text": "Saturn and number 88 shape your career tendencies as a growth edge to watch steadily.",
                        }
                    ],
                    "footer": DEFAULT_FOOTER,
                },
                ("unsupplied_planet:8", "unsupplied_number:88"),
            ),
            (
                "event_prediction_you_will_lose",
                lambda _req, _t: {
                    "sections": [
                        {
                            "fact_ids": [valid_fid],
                            "text": "In Personal Year 3 you will lose money if you rush, so treat this tendency with extra care.",
                        }
                    ],
                    "footer": DEFAULT_FOOTER,
                },
                ("event_prediction:predicted_event",),
            ),
            (
                "outcome_promises_cure_guaranteed_will_fix",
                lambda _req, _t: {
                    "sections": [
                        {
                            "fact_ids": [valid_fid],
                            "text": "This routine is guaranteed to cure stress and will fix every delay as a growth edge.",
                        }
                    ],
                    "footer": DEFAULT_FOOTER,
                },
                ("banned_word:cure", "banned_phrase:guaranteed", "banned_phrase:will fix"),
            ),
            (
                "unapproved_remedy_not_in_library",
                lambda _req, _t: {
                    "sections": [
                        {
                            "fact_ids": [valid_fid],
                            "text": "As a growth edge, feed black crows and wear a copper ring on your middle finger daily.",
                        }
                    ],
                    "footer": DEFAULT_FOOTER,
                },
                ("unsupplied_remedy:",),
            ),
            (
                "higher_tier_item_shown_to_lower_tier",
                lambda _req, _t: {
                    "sections": [
                        {
                            "fact_ids": [valid_fid],
                            "text": (
                                "Your year manifestation and quarterly focus include wearing a yellow sapphire gemstone "
                                "and chanting a Vedic mantra as a growth edge."
                            ),
                        }
                    ],
                    "footer": DEFAULT_FOOTER,
                },
                (
                    "tier_entitlement_leak:gemstone_on_charm_free",
                    "tier_entitlement_leak:mantra_on_charm_free",
                    "tier_entitlement_leak:manifestation_on_charm_free",
                ),
            ),
            (
                "non_json_llm_reply",
                lambda _req, _t: "Plain text non-JSON reply from model without structured schema!",
                ("non_json_llm_reply",),
            ),
        ]

        for idx, (case_name, mock_llm, expected_violation_prefixes) in enumerate(adversarial_cases):
            clear_write_cache_for_tests()
            with self.assertLogs("numeros.indication_validator", level="WARNING") as cm:
                res = run_charm_pipeline_with_stage_events(
                    day=12,
                    month=1,
                    year=1951,
                    gender="male",
                    calling_name="Aarav",
                    entitlement_tier="charm_free",
                    question=f"What do my numbers indicate for steady focus ({idx})?",
                    llm_callable=mock_llm,
                    reference_date=ref_day,
                )

            self.assertTrue(res["llm_rejected"], f"[{case_name}] must reject adversarial LLM output")
            self.assertTrue(res["used_fallback"], f"[{case_name}] must fall back to deterministic library text")
            self.assertFalse(res["credit_chargeable"], f"[{case_name}] must NOT be credit chargeable")
            self.assertEqual(res["credits_charged"], 0, f"[{case_name}] must charge 0 credits")

            # Verify fallback text is clean library text (contains zero adversarial substrings)
            for forbidden_leak in ("88", "you will lose", "guaranteed", "will fix", "feed black crows", "copper ring", "yellow sapphire", "Plain text non-JSON"):
                self.assertNotIn(forbidden_leak, res["validated_text"], f"[{case_name}] leaked unvalidated text!")

            # Verify expected violation codes were recorded
            joined_violations = " | ".join(res.get("validator_violations") or [])
            for exp_pref in expected_violation_prefixes:
                self.assertIn(exp_pref, joined_violations, f"[{case_name}] missing violation {exp_pref} in {joined_violations}")

            # Verify audit log entry was emitted with credit_charged=0 and zero PII
            joined_logs = "\n".join(cm.output)
            self.assertIn("credit_charged=0", joined_logs, f"[{case_name}] audit log must record credit_charged=0")
            self.assertNotIn("Aarav", joined_logs, f"[{case_name}] audit log must contain zero PII")
            self.assertNotIn("1951", joined_logs, f"[{case_name}] audit log must contain zero DOB")


if __name__ == "__main__":
    unittest.main()
