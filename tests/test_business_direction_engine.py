"""
Unit tests for Business Direction Intelligence & Existing Business Alignment Engine (Section 1.A & 1.B).
Verifies separation of commercial viability from traditional frameworks,
handling of unknown birth data, and prioritization of practical business improvements.
"""

import unittest
from app.engine.business_direction_engine import (
    BusinessDirectionEngine,
    FounderProfile,
    CandidateBusinessOption,
)


class TestBusinessDirectionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BusinessDirectionEngine()

    def test_startup_evaluation_commercial_viability(self):
        """Commercial viability checks skills and capital sufficiency independently."""
        founder = FounderProfile(
            name="Alex Mercer",
            skills=["product_management", "software_engineering"],
            experience_years=8,
            capital_band="growth_50k_250k",
            location="Bangalore",
            risk_tolerance="moderate",
            operating_preference="digital_remote",
            dob="1990-05-15",
        )
        option = CandidateBusinessOption(
            idea_id="opt_saas_01",
            name="PulseFlow Cloud",
            activity_description="SaaS workflow automation software for remote product teams",
            revenue_model="subscription",
            customer_segment="technology companies",
            delivery_channel="cloud_web_app",
            estimated_startup_capital_required="seed_10k_50k",
        )

        result = self.engine.evaluate_startup_option(founder, option)
        # Commercial checks
        self.assertTrue(result.commercial_viability.skill_match)
        self.assertTrue(result.commercial_viability.capital_sufficient)
        self.assertEqual(result.commercial_viability.operational_complexity, "low")
        self.assertEqual(result.synthesis_recommendation, "COMMERCIALLY_VIABLE")
        # Evidence disclaimer
        self.assertIn("Evidence Notice", result.mandatory_disclaimer)

    def test_startup_evaluation_skill_and_capital_gap(self):
        """Identifies commercial gaps when founder lacks skills or capital runway."""
        founder = FounderProfile(
            name="Samir Khan",
            skills=["graphic_design"],
            experience_years=1,
            capital_band="bootstrapped",
            location="Mumbai",
            risk_tolerance="low",
            operating_preference="hands_on_operations",
            dob=None,  # Missing DOB!
        )
        option = CandidateBusinessOption(
            idea_id="opt_hardware_01",
            name="Titan Robotics",
            activity_description="Industrial robotics and semiconductor fabrication hardware",
            revenue_model="hardware_manufacturing",
            customer_segment="automotive factories",
            delivery_channel="direct_b2b",
            estimated_startup_capital_required="institutional_250k_plus",
        )

        result = self.engine.evaluate_startup_option(founder, option)
        # Commercial gaps
        self.assertFalse(result.commercial_viability.capital_sufficient)
        self.assertEqual(result.commercial_viability.operational_complexity, "high")
        self.assertEqual(result.synthesis_recommendation, "COMMERCIAL_PREREQUISITES_REQUIRED")
        # Missing DOB must be marked insufficient_evidence, never guessed
        self.assertEqual(result.traditional_alignment.alignment_status, "insufficient_evidence")
        self.assertTrue(any("No founder date of birth provided" in u for u in result.traditional_alignment.unknowns))

    def test_diagnose_existing_business_fixed_vs_changeable(self):
        """Diagnose distinguishes fixed constraints from changeable factors and prioritizes practical improvements."""
        diag = self.engine.diagnose_existing_business(
            legal_name="Apex Healthcare Private Limited",
            trading_name="Apex Vitality Clinic",
            products_services="Outpatient clinical care and medical diagnostics",
            current_constraints=[
                "5-year hospital commercial lease signed",
                "State medical board healthcare facility license",
            ],
            performance_challenges=[
                "Customer retention dropping in Q3",
                "Cash flow delay from insurance reimbursements",
            ],
        )
        # Verify fixed vs changeable separation
        fixed = diag["fixed_vs_changeable"]["fixed_constraints"]
        self.assertTrue(any("lease" in f.lower() for f in fixed))
        self.assertTrue(any("license" in f.lower() for f in fixed))

        # Practical improvements first
        improvements = diag["practical_improvements_first"]
        self.assertTrue(any("payment collection" in i.lower() or "retention" in i.lower() for i in improvements))

        # Traditional remedies must be optional with cost disclosure
        remedies = diag["traditional_remedies"]
        for r in remedies:
            self.assertFalse(r["mandatory"])
            self.assertIn("cost_estimate", r)
            self.assertIn("disclaimer", r)

        self.assertIn("Statutory Disclosure", diag["statutory_notice"])


if __name__ == "__main__":
    unittest.main()
