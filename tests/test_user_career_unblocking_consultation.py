"""
tests/test_user_career_unblocking_consultation.py
=================================================
Automated verification for user questions:
1. "What does my Birth Number (Driver) say about my career growth and opportunities?"
2. "I feel stuck in my career and lost opportunities. How can I unblock my professional growth?"

Validates:
- Non-identical, distinct, humanized consultation dialogues.
- Zero canned fallback text.
- Empathetic master numerologist dialogue grounded in deterministic calculations.
- Presence of 7-tier prediction models and cards.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestUserCareerUnblockingConsultation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_distinct_humanized_responses_for_user_questions(self):
        # User profile: Born 15-08-1990 (Driver 6, Conductor 6+8+1=6 or 15/8/1990 -> 1+5+8+1+9+9+0 = 33 -> 6)
        payload_base = {
            "name": "Arjun Sharma",
            "day": 15,
            "month": 8,
            "year": 1990,
            "user_id": "test_seeker_arjun"
        }

        # Query 1: Driver Meaning
        q1 = "What does my Birth Number (Driver) say about my career growth and opportunities?"
        res1 = self.client.post("/api/v1/readings/ask", json={**payload_base, "question": q1})
        self.assertEqual(res1.status_code, 200)
        data1 = res1.json()

        ans1 = data1.get("direct_answer", "")
        self.assertTrue(len(ans1) > 100)
        self.assertNotIn("In classical numerology, every cycle brings distinct lessons. Focus on balancing your Driver energy with conscious daily reflection.", ans1)
        self.assertIn("Driver 6", ans1)
        self.assertIn("Venus", ans1)
        self.assertIn("The Logic Behind Your Numbers", ans1)
        self.assertIn("Three Practical Actions", ans1)

        # Query 2: Stuck in Career & Lost Opportunities
        q2 = "I feel stuck in my career and lost opportunities. How can I unblock my professional growth?"
        res2 = self.client.post("/api/v1/readings/ask", json={**payload_base, "question": q2})
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()

        ans2 = data2.get("direct_answer", "")
        self.assertTrue(len(ans2) > 100)
        self.assertNotIn("In classical numerology, every cycle brings distinct lessons. Focus on balancing your Driver energy with conscious daily reflection.", ans2)
        self.assertIn("stuck", ans2.lower())
        self.assertIn("The Logic Behind Your Numbers", ans2)
        self.assertIn("Three Practical Actions to Unblock Your Growth", ans2)

        # Confirm they are completely distinct responses, not identical canned text
        self.assertNotEqual(ans1, ans2)

        # Confirm charm_prediction model is present with human_friendly structure
        self.assertIn("charm_prediction", data1)
        self.assertIn("charm_prediction", data2)
        self.assertIn("human_friendly", data1["charm_prediction"])
        self.assertIn("human_friendly", data2["charm_prediction"])

if __name__ == "__main__":
    unittest.main()
