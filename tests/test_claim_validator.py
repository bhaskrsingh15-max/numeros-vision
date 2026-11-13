import sys
import os
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.engine.claim_validator import (
    lint_copy, validate_claims_and_hallucination_gate, ClaimNode
)
from app.engine.rule_registry import (
    get_rule, resolve_rule_conflict, RULE_REGISTRY
)

class TestClaimValidatorAndRuleRegistry(unittest.TestCase):

    def test_copy_linter_detects_banned_words(self):
        """Clauses 56 & 228: Must flag banned words (unlock, elevate, game-changer, revolutionary, seamless)."""
        bad_copy = "Unlock your destiny today with this revolutionary game-changer reading to elevate your life seamlessly!"
        res = lint_copy(bad_copy)
        self.assertFalse(res.is_valid)
        banned = [w.lower() for w in res.banned_words_found]
        self.assertTrue(any("unlock" in w for w in banned))
        self.assertTrue(any("revolutionary" in w for w in banned))
        self.assertTrue(any("game-changer" in w or "game changer" in w for w in banned))
        self.assertTrue(any("elevate" in w for w in banned))
        self.assertTrue(any("seamless" in w for w in banned))

    def test_copy_linter_enforces_exact_tagline(self):
        """Clause 1 & 226: Must enforce exact spelling 'Anveil Every Charm'."""
        bad_tagline = "Numeros Vision — Unveil Every Charm"
        res = lint_copy(bad_tagline)
        self.assertFalse(res.tagline_valid)
        self.assertIn("Anveil Every Charm", res.remediated_text)

        good_tagline = "Numeros Vision — Anveil Every Charm"
        res2 = lint_copy(good_tagline)
        self.assertTrue(res2.tagline_valid)

    def test_copy_linter_flags_fabricated_statistics(self):
        """Clauses 58 & 60: Fabricated stats like '99% accurate' must be flagged and replaced with [INSERT REAL FIGURE]."""
        fake_stat_copy = "Our AI system is 99% accurate with over 50,000 satisfied customers."
        res = lint_copy(fake_stat_copy)
        self.assertFalse(res.is_valid)
        self.assertTrue(len(res.fabricated_stats_found) > 0)
        self.assertIn("[INSERT REAL FIGURE]", res.remediated_text)

    def test_copy_linter_blocks_medical_and_financial_guarantees(self):
        """Clauses 40, 41, 42: Medical diagnoses/cures and guaranteed financial returns must be blocked."""
        medical_copy = "This ruby gemstone cures heart disease and heals illnesses so you can stop taking medicine."
        res_med = lint_copy(medical_copy)
        self.assertFalse(res_med.is_valid)
        self.assertTrue(any("health" in v for v in res_med.safety_violations))

        financial_copy = "This number combination provides a guaranteed profit in intraday trade and jackpot returns."
        res_fin = lint_copy(financial_copy)
        self.assertFalse(res_fin.is_valid)
        self.assertTrue(any("financial" in v for v in res_fin.safety_violations))

    def test_hallucination_gate_empty_canvas_rule(self):
        """Clauses 35 & 36: Empty Canvas Rule — every claim must map to calculation, rule, or verified source."""
        valid_calcs = {"calc_driver_1", "calc_conductor_4"}
        valid_rules = {"RULE_DRIVER_CALC_V1", "RULE_CONDUCTOR_CALC_V1"}
        valid_sources = {"SOURCE_TN_DIPLOMA_P42"}

        grounded_claims = [
            ClaimNode(
                claim_id="c1",
                text="Driver number is 1 representing leadership and authority.",
                calculation_ref="calc_driver_1",
                rule_id="RULE_DRIVER_CALC_V1",
                source_ref="SOURCE_TN_DIPLOMA_P42"
            )
        ]

        verdict_pass = validate_claims_and_hallucination_gate(
            claims=grounded_claims,
            full_output_text="Your Driver number is 1, indicating authority and initiative. Anveil Every Charm.",
            valid_calculation_ids=valid_calcs,
            valid_rule_ids=valid_rules,
            valid_source_ids=valid_sources
        )
        self.assertTrue(verdict_pass.passed)
        self.assertEqual(verdict_pass.stage_reached, 12)

        # Now test an ungrounded hallucination
        hallucinated_claims = [
            ClaimNode(
                claim_id="c2",
                text="You will encounter an alien contact in year 2029.",
                calculation_ref="non_existent_calc",
                rule_id="non_existent_rule",
                source_ref=None
            )
        ]

        verdict_fail = validate_claims_and_hallucination_gate(
            claims=hallucinated_claims,
            full_output_text="Alien contact prediction.",
            valid_calculation_ids=valid_calcs,
            valid_rule_ids=valid_rules,
            valid_source_ids=valid_sources
        )
        self.assertFalse(verdict_fail.passed)
        self.assertEqual(verdict_fail.stage_reached, 10)
        self.assertIn("Empty Canvas Violation", verdict_fail.reason)

    def test_rule_registry_and_conflict_resolution(self):
        """Clauses 33 & 137: Authoritative rule retrieval and deterministic conflict resolution."""
        rule_driver = get_rule("RULE_DRIVER_CALC_V1")
        self.assertIsNotNone(rule_driver)
        self.assertEqual(rule_driver.version, "TN-PRO-V1")
        self.assertEqual(rule_driver.priority, 100)

        # Conflict resolution between priority 100 and priority 90
        resolved = resolve_rule_conflict(["RULE_DRIVER_CALC_V1", "RULE_MOBILE_MALEFIC_PAIRS_V1"])
        self.assertEqual(resolved.rule_id, "RULE_DRIVER_CALC_V1")

if __name__ == "__main__":
    unittest.main()
