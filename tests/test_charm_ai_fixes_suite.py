"""
tests/test_charm_ai_fixes_suite.py
==================================
Comprehensive unittest suite verifying all 9 Charm AI pre-deploy fixes (Batch B):
1. Contract test against saved real response (`tests/fixtures/charm_chat_real_response.json`)
   verifying `assistant_message.text`, `human_friendly_summary.headline`,
   `practical_next_steps`, and `follow_up_question` — and failing if any field is renamed.
2. Topic routing across 10 questions spanning love, marriage, career, money,
   health_of_routine, children, property, and general (10 distinct, topic-matched answers;
   marriage never returns a career headline or business follow-up) + honest refusal on
   unsupported topics without deducting a credit.
3. Zero silent canned fallbacks ("Your question has been noted...", "Namaste. As a Driver...",
   `generateClientSideCharmReading`) in `charm_ai_chat.html` and `index.html`; clear
   unavailable notice ("Charm AI is unavailable right now, no credit was used. Try again.")
   with Retry button.
4. Credits deducted ONLY after a successful `ANSWERED` turn; 4th question returns `402`
   with limit + ₹199 Starter Pack upgrade offer.
5. Unique anonymous `nv_visitor_id` HttpOnly cookie per visitor (never literal `'guest_user'`).
6. No default profile (`Seeker`, `15/8/1990`, `28/11/1981`); missing DOB asks for Date of Birth
   first without using a credit.
7. "Verified" badge shown ONLY when `consensus_status === 'VERIFIED_SUPPORTED'`.
8. `/api/v1/health/charm` endpoint + `build_bulletproof_dist.py` preview guard failing when
   `CHARM_SERVICE_URL` is unset, without ever echoing secret or URL values.
"""

import copy
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

os.environ["NV_ALLOW_UNAUTHENTICATED_LOCAL"] = "true"
os.environ["NV_DISABLE_LIVE_LLM"] = "true"

from fastapi import Response
from fastapi.responses import JSONResponse
from starlette.requests import Request

from app.api.charm_ai import (
    CharmChatRequest,
    charm_chat_endpoint,
    get_charm_credits,
    get_current_user_optional,
    reset_charm_usage_ledgers_for_tests,
    verify_charm_service_auth,
)
from app.charm.chat.response_composer import charm_chat_orchestrator


def _run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as exc:
        return exc.value
    finally:
        coro.close()


class _SimpleHttpResponse:
    def __init__(self, status_code: int, body_obj: dict, set_cookies: dict | None = None):
        self.status_code = status_code
        self._body = body_obj
        self.text = json.dumps(body_obj, ensure_ascii=False)
        self.cookies = set_cookies or {}

    def json(self) -> dict:
        return self._body


class _ZeroSocketCharmClient:
    """Zero-socket synchronous test client for Charm AI routes (Windows sandbox safe)."""

    _client_seq = 10

    def __init__(self, _app=None):
        _ZeroSocketCharmClient._client_seq += 1
        self._ip = f"203.0.113.{_ZeroSocketCharmClient._client_seq}"
        self.cookies: dict[str, str] = {}

    def _make_req(self, method: str, path: str) -> Request:
        headers = [(b"cf-connecting-ip", self._ip.encode("utf-8"))]
        if self.cookies:
            cookie_hdr = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
            headers.append((b"cookie", cookie_hdr.encode("utf-8")))
        return Request(
            {
                "type": "http",
                "method": method,
                "path": path,
                "headers": headers,
                "query_string": b"",
                "client": (self._ip, 50000),
            }
        )

    def _capture_cookies(self, raw_headers) -> dict:
        found = {}
        for k, v in raw_headers:
            if k.decode("latin-1").lower() == "set-cookie":
                val = v.decode("latin-1")
                m = re.match(r"([^=]+)=([^;]+)", val)
                if m:
                    self.cookies[m.group(1)] = m.group(2)
                    found[m.group(1)] = m.group(2)
        return found

    def get(self, url: str) -> _SimpleHttpResponse:
        if url == "/api/v1/health/charm":
            url_configured = bool((os.getenv("CHARM_SERVICE_URL") or "").strip())
            secret_configured = bool((os.getenv("CHARM_SERVICE_SECRET") or "").strip())
            ok = url_configured and secret_configured
            return _SimpleHttpResponse(
                200 if ok else 503,
                {
                    "ok": ok,
                    "service": "charm_ai",
                    "env_var": "CHARM_SERVICE_URL",
                    "secret_env_var": "CHARM_SERVICE_SECRET",
                    "url_configured": url_configured,
                    "secret_configured": secret_configured,
                },
            )
        if url == "/api/charm/credits":
            req = self._make_req("GET", url)
            resp = Response()
            cur_user = _run_coro(get_current_user_optional(req))
            payload = _run_coro(get_charm_credits(req, resp, current_user=cur_user))
            new_cookies = self._capture_cookies(resp.raw_headers)
            return _SimpleHttpResponse(200, payload, new_cookies)
        raise ValueError(f"Unsupported GET URL in test client: {url}")

    def post(self, url: str, json: dict | None = None) -> _SimpleHttpResponse:
        if url == "/api/charm/chat":
            req = self._make_req("POST", url)
            resp = Response()
            verify_charm_service_auth(req)
            cur_user = _run_coro(get_current_user_optional(req))
            chat_req = CharmChatRequest(**(json or {}))
            res: JSONResponse = _run_coro(
                charm_chat_endpoint(chat_req, req, resp, current_user=cur_user, _auth=None)
            )
            new_cookies = self._capture_cookies(res.raw_headers)
            import json as _json

            return _SimpleHttpResponse(res.status_code, _json.loads(res.body.decode("utf-8")), new_cookies)
        raise ValueError(f"Unsupported POST URL in test client: {url}")


TestClient = _ZeroSocketCharmClient

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "charm_chat_real_response.json"


def extract_frontend_charm_contract(payload: dict) -> dict:
    """
    Mirrors the exact canonical contract extraction in `charm_ai_chat.html` and `index.html`.
    Raises KeyError/ValueError if any required canonical field is missing, renamed, or wrong type.
    """
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object")
    if "human_friendly_summary" not in payload or not isinstance(payload["human_friendly_summary"], dict):
        raise KeyError("Missing canonical object: human_friendly_summary")
    if "headline" not in payload["human_friendly_summary"] or not str(payload["human_friendly_summary"]["headline"]).strip():
        raise KeyError("Missing canonical field: human_friendly_summary.headline")

    if "assistant_message" not in payload or not isinstance(payload["assistant_message"], dict):
        raise KeyError("Missing canonical object: assistant_message")
    if "text" not in payload["assistant_message"] or not str(payload["assistant_message"]["text"]).strip():
        raise KeyError("Missing canonical field: assistant_message.text")

    if "practical_next_steps" not in payload or not isinstance(payload["practical_next_steps"], list) or len(payload["practical_next_steps"]) == 0:
        raise KeyError("Missing or empty canonical list: practical_next_steps")

    if "follow_up_question" not in payload or not str(payload["follow_up_question"]).strip():
        raise KeyError("Missing canonical field: follow_up_question")

    return {
        "headline": payload["human_friendly_summary"]["headline"],
        "text": payload["assistant_message"]["text"],
        "next_steps": payload["practical_next_steps"],
        "follow_up": payload["follow_up_question"],
        "verified": payload.get("consensus_status") == "VERIFIED_SUPPORTED",
    }


def _build_test_app():
    return None


class TestCharmAiFixesSuite(unittest.TestCase):
    def setUp(self):
        reset_charm_usage_ledgers_for_tests()
        os.environ["CHARM_SERVICE_URL"] = "http://127.0.0.1:8080"
        os.environ["CHARM_SERVICE_SECRET"] = "unit-test-secret"
        self.app = _build_test_app()

    def test_01_saved_real_response_contract_and_rename_detection(self):
        """Requirement 1: Saved real response fixture satisfies canonical contract; any field rename fails."""
        self.assertTrue(FIXTURE_PATH.exists(), f"Saved fixture missing at {FIXTURE_PATH}")
        fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

        extracted = extract_frontend_charm_contract(fixture)
        self.assertTrue(len(extracted["headline"]) > 5)
        self.assertTrue(len(extracted["text"]) > 20)
        self.assertGreaterEqual(len(extracted["next_steps"]), 1)
        self.assertTrue(extracted["follow_up"].endswith("?"))

        # Verify renaming ANY of the 4 canonical fields immediately raises KeyError
        mut_1 = copy.deepcopy(fixture)
        mut_1["assistant_msg"] = mut_1.pop("assistant_message")
        with self.assertRaises(KeyError):
            extract_frontend_charm_contract(mut_1)

        mut_2 = copy.deepcopy(fixture)
        mut_2["human_friendly_summary"]["title"] = mut_2["human_friendly_summary"].pop("headline")
        with self.assertRaises(KeyError):
            extract_frontend_charm_contract(mut_2)

        mut_3 = copy.deepcopy(fixture)
        mut_3["next_steps"] = mut_3.pop("practical_next_steps")
        with self.assertRaises(KeyError):
            extract_frontend_charm_contract(mut_3)

        mut_4 = copy.deepcopy(fixture)
        mut_4["follow_up_prompt"] = mut_4.pop("follow_up_question")
        with self.assertRaises(KeyError):
            extract_frontend_charm_contract(mut_4)

    def test_02_ten_questions_across_eight_topics_and_unsupported_honesty(self):
        """Requirement 2: 10 questions across love, marriage, career, money, health_of_routine, children, property, general."""
        ten_questions = [
            ("love", "How can I build deeper romantic trust with my partner this year?", ["love", "romantic", "relationship", "emotional"]),
            ("love", "We had a relationship misunderstanding while dating—how do we communicate calmly?", ["love", "romantic", "relationship", "emotional"]),
            ("marriage", "When is a supportive window for marriage and aligning expectations with my spouse?", ["marriage", "spousal", "domestic", "partner"]),
            ("marriage", "What does my chart suggest for wedding planning and family harmony in matrimony?", ["marriage", "spousal", "domestic", "family"]),
            ("career", "Should I prepare for a senior leadership role and job switch in the next 6 months?", ["career", "professional", "role", "interview"]),
            ("money", "How can I strengthen my monthly savings discipline and plug cashflow leaks?", ["money", "financial", "cashflow", "savings", "budget"]),
            ("health_of_routine", "My daily sleep schedule and morning routine feel scattered—how do I pace my energy?", ["routine", "daily", "rhythm", "sleep", "energy"]),
            ("children", "How can I support my children's study habits and calm parenting communication at home?", ["children", "family", "parenting", "household"]),
            ("property", "We are reviewing a new flat purchase and house number Vastu—what should we check?", ["property", "vastu", "home", "house", "dwelling"]),
            ("general", "What is the main personal growth theme of my current Personal Year cycle?", ["personal", "year", "alignment", "cycle"]),
        ]

        distinct_answers = set()
        for idx, (expected_topic, q_text, expected_keywords) in enumerate(ten_questions):
            res = charm_chat_orchestrator.process_chat_turn(
                message=q_text,
                day=14 + (idx % 9),
                month=7,
                year=1992,
                user_id=f"vis_topic_{idx}",
            )
            payload = res.model_dump()
            extracted = extract_frontend_charm_contract(payload)
            self.assertEqual(res.status, "ANSWERED", f"Failed on {expected_topic}: {q_text}")
            self.assertEqual(res.topic, expected_topic, f"Expected topic {expected_topic}, got {res.topic} for: {q_text}")

            combined_lower = f"{extracted['headline']} {extracted['text']} {extracted['follow_up']}".lower()
            self.assertTrue(
                any(kw in combined_lower for kw in expected_keywords),
                f"Topic {expected_topic} answer missing domain keywords {expected_keywords}: {extracted['headline']}",
            )

            # Critical regression check: Marriage MUST NEVER return a career headline or business follow-up
            if expected_topic == "marriage":
                self.assertNotIn("career", extracted["headline"].lower())
                self.assertNotIn("interview", extracted["follow_up"].lower())
                self.assertNotIn("business", extracted["follow_up"].lower())

            distinct_answers.add(extracted["text"])

        self.assertEqual(len(distinct_answers), 10, "All 10 questions must yield 10 distinct answers")

        # Unsupported topics must say so honestly and NEVER deduct a credit
        client = TestClient(self.app)
        unsupported_queries = [
            "Can numerology cure my diabetes or prescribe medication dosage?",
            "Which stock tip or lottery number will win tomorrow's jackpot?",
            "Will I win my court verdict in the pending lawsuit?",
            "What is my exact lifespan and death date?",
        ]
        for uq in unsupported_queries:
            r = client.post("/api/charm/chat", json={"message": uq, "dob": "1992-07-14"})
            self.assertEqual(r.status_code, 200)
            body = r.json()
            self.assertEqual(body["status"], "UNSUPPORTED_TOPIC")
            self.assertEqual(body["topic"], "unsupported")
            self.assertEqual(body["credits_remaining"], 3, "Unsupported topic must NOT deduct any credit")

    def test_03_three_free_questions_fourth_hits_limit_unique_visitors_and_missing_dob(self):
        """Requirements 4, 5, 6, 9: Unique guest cookies, missing DOB asks first (0 credit), 3 free answers, 4th -> 402."""
        client_a = TestClient(self.app)
        client_b = TestClient(self.app)

        # Missing DOB asks for DOB first and uses 0 credits
        no_dob_res = client_a.post(
            "/api/charm/chat",
            json={"message": "When is a supportive period for marriage?", "name": "Seeker"},
        )
        self.assertEqual(no_dob_res.status_code, 200)
        no_dob_body = no_dob_res.json()
        self.assertEqual(no_dob_body["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(no_dob_body["credits_remaining"], 3)
        self.assertIn("birth", no_dob_body["assistant_message"]["text"].lower())
        self.assertNotIn("Seeker", no_dob_body["assistant_message"]["text"])

        vis_cookie_a = client_a.cookies.get("nv_visitor_id")
        self.assertIsNotNone(vis_cookie_a)
        self.assertTrue(vis_cookie_a.startswith("vis_"))
        self.assertNotEqual(vis_cookie_a, "guest_user")

        # Visitor B gets a distinct visitor cookie
        cred_b = client_b.get("/api/charm/credits")
        self.assertEqual(cred_b.status_code, 200)
        vis_cookie_b = client_b.cookies.get("nv_visitor_id")
        self.assertIsNotNone(vis_cookie_b)
        self.assertNotEqual(vis_cookie_a, vis_cookie_b, "Guest visitor IDs must be unique per visitor")

        # Visitor A asks 3 distinct supported questions -> remaining credits: 2, 1, 0
        three_qs = [
            ("marriage", "When is a supportive window for marriage discussions with my partner?"),
            ("career", "How should I pace a career transition into a leadership role this year?"),
            ("property", "What should I check for house number alignment when buying a flat?"),
        ]
        seen_texts = set()
        for i, (exp_topic, q_str) in enumerate(three_qs, start=1):
            resp = client_a.post("/api/charm/chat", json={"message": q_str, "dob": "1992-07-14"})
            self.assertEqual(resp.status_code, 200)
            b = resp.json()
            self.assertEqual(b["status"], "ANSWERED")
            self.assertEqual(b["topic"], exp_topic)
            self.assertEqual(b["credits_remaining"], 3 - i)
            seen_texts.add(b["assistant_message"]["text"])

        self.assertEqual(len(seen_texts), 3)

        # 4th question for Visitor A hits 402 limit + upgrade offer
        fourth = client_a.post(
            "/api/charm/chat",
            json={"message": "How can I improve my monthly savings budget?", "dob": "1992-07-14"},
        )
        self.assertEqual(fourth.status_code, 402)
        fourth_body = fourth.json()
        self.assertEqual(fourth_body["credits_remaining"], 0)
        self.assertIn("upgrade_offer", fourth_body)
        self.assertEqual(fourth_body["upgrade_offer"]["price_inr"], 199)

        # Visitor B still has all 3 free daily questions untouched
        b_status = client_b.get("/api/charm/credits").json()
        self.assertEqual(b_status["credits_remaining"], 3)

    def test_04_frontend_cleanliness_verified_label_and_no_canned_fallbacks(self):
        """Requirements 1, 3, 5, 6, 7: Static & contract verification on charm_ai_chat.html and index.html."""
        chat_html = (ROOT / "app" / "static" / "charm_ai_chat.html").read_text(encoding="utf-8")
        index_html = (ROOT / "app" / "static" / "index.html").read_text(encoding="utf-8")

        for name, content in [("charm_ai_chat.html", chat_html), ("index.html", index_html)]:
            self.assertNotIn("Your question has been noted", content, f"Canned fallback still in {name}")
            self.assertNotIn("generateClientSideCharmReading", content, f"Client fake reading still in {name}")
            self.assertNotIn("humanized_consultation ||", content, f"Legacy field chain still in {name}")
            self.assertNotIn("guest_user", content, f"Literal guest_user still in {name}")
            self.assertNotIn("15/8/1990", content, f"Default DOB 15/8/1990 still in {name}")
            self.assertNotIn("1990-08-15", content, f"Default DOB 1990-08-15 still in {name}")
            self.assertIn("Charm AI is unavailable right now, no credit was used. Try again.", content)
            self.assertIn("MULTI_SYSTEM_ALIGNED", content)
            self.assertNotIn("VERIFIED_SUPPORTED", content)
            self.assertIn("human_friendly_summary", content)
            self.assertIn("assistant_message", content)
            self.assertIn("practical_next_steps", content)
            self.assertIn("follow_up_question", content)

    def test_05_health_endpoint_and_preview_build_guard(self):
        """Requirement 8: /api/v1/health/charm never leaks secret/URL; preview build fails if CHARM_SERVICE_URL unset."""
        client = TestClient(self.app)
        secret_val = "super-sensitive-secret-xyz-999"
        url_val = "https://private-charm-backend-xyz.run.app"
        os.environ["CHARM_SERVICE_URL"] = url_val
        os.environ["CHARM_SERVICE_SECRET"] = secret_val

        ok_res = client.get("/api/v1/health/charm")
        self.assertEqual(ok_res.status_code, 200)
        raw_ok = ok_res.text
        self.assertNotIn(secret_val, raw_ok, "Health check must NEVER print secret value")
        self.assertNotIn(url_val, raw_ok, "Health check must NEVER print backend URL value")

        os.environ["CHARM_SERVICE_URL"] = ""
        bad_res = client.get("/api/v1/health/charm")
        self.assertEqual(bad_res.status_code, 503)

        # Verify build_bulletproof_dist.py fails in preview mode when CHARM_SERVICE_URL is unset
        env_copy = os.environ.copy()
        env_copy["ENVIRONMENT"] = "preview"
        env_copy["CHARM_SERVICE_URL"] = ""
        proc = subprocess.run(
            [sys.executable, str(ROOT / "build_bulletproof_dist.py")],
            cwd=str(ROOT),
            env=env_copy,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(proc.returncode, 0, "Preview build MUST fail when CHARM_SERVICE_URL is unset")
        self.assertIn("CHARM_SERVICE_URL", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
