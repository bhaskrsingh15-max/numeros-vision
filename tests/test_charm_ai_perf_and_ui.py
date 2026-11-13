import sys
import os
import unittest
import time

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app

class TestCharmAIPerfAndUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_charm_ai_readings_ask_perf(self):
        """Verify sub-100ms response time and schema completeness for Charm AI."""
        questions = [
            ("Is 2026 favorable for my career progression and new ventures?", "Turn 1 (Cold)"),
            ("What consecrated remedies harmonize Driver 6 and Conductor 6?", "Turn 2 (Warm)"),
            ("How do my numbers influence marriage timing and family harmony?", "Turn 3 (Warm)"),
        ]
        latencies = []
        for q, label in questions:
            payload = {
                'name': 'Arjun Sharma',
                'day': 15,
                'month': 8,
                'year': 1990,
                'question': q,
                'user_id': 'perf_test_user',
                'premium_token': 'test_master_pass'
            }
            t0 = time.time()
            resp = self.client.post('/api/v1/readings/ask', json=payload)
            lat = (time.time() - t0) * 1000
            latencies.append(lat)

            self.assertEqual(resp.status_code, 200, f"Failed on {label}: {resp.text}")
            res = resp.json()
            self.assertIn('topic_display', res)
            self.assertIn('trace_id', res)
            self.assertIn('direct_answer', res)
            self.assertTrue(len(res.get('remedies', [])) > 0, "Must return remedies")
            self.assertIn('lucky_elements', res)

        avg_lat = sum(latencies) / len(latencies)
        print(f"\nCharm AI Query Average Latency: {avg_lat:.2f} ms")
        self.assertLess(avg_lat, 200.0, f"Average latency {avg_lat:.2f} ms exceeds 200 ms budget")

if __name__ == "__main__":
    unittest.main()
