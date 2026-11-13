import sys
import os
import unittest
import json

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app

class TestCheiroRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.test_cases = [
            # Case 1: Unaligned first name (Rahul = Root 8 Saturn, not in {1,3,5,6})
            ("Rahul Sharma", "1987-11-07", False),
            # Case 2: Unaligned first & overall (Elon = 2 Moon, Elon Musk = 8 Saturn anti to 1 Sun)
            ("Elon Musk", "1971-06-28", False),
            # Case 3: Anti combination (Name root 6 Venus with Driver 3 Jupiter - mutually anti!)
            ("Vikram Singh", "1992-03-12", False),
            # Case 4: Perfectly aligned (Raahull = 3 Jupiter, Raahull Sharma = 1 Sun, non-anti to Driver 7, Cond 7)
            ("Raahull Sharma", "1987-11-07", True),
        ]

    def test_cheiro_chaldean_name_balancing_rules(self):
        """Verify Cheiro Chaldean name balancing rules, driver/conductor calculation, and sanctuary policy."""
        for name, dob, expected_aligned in self.test_cases:
            resp = self.client.post(
                "/api/v2/numerology/name/balance",
                json={"full_name": name, "dob_str": dob}
            )
            self.assertEqual(resp.status_code, 200, f"Failed for {name}: {resp.text}")
            obj = resp.json()
            ev = obj["current_name_evaluation"]
            d = obj["calculated_driver"]
            c = obj["calculated_conductor"]
            is_al = obj["is_aligned"]
            score = ev["total_score"]

            self.assertEqual(
                is_al, expected_aligned,
                f"Mismatch for {name} (D:{d}, C:{c}): got {is_al}, expected {expected_aligned} (score: {score})"
            )

        # Sanctuary Policy: No automated balancing candidates on customer-facing app
        self.assertEqual(len(obj.get("suggested_candidates", [])), 0, "Candidates must be empty on app!")

if __name__ == "__main__":
    unittest.main()
