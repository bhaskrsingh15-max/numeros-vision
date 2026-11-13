"""
Step 2 Automated Verification Suite — Logo Intelligence Rule Set v1 (`test_logo_rulebook_v1.py`)
Tests:
1. Read-only binding & parity with `NUMBER_REGISTRY` (`1..9`), rejecting master numbers (`11, 22, 33`).
2. Locked Decision D6: Client palettes follow client numerology tables (no blanket navy or black ban).
3. Measured contrast thresholds (`#C9A227` on `#FFFDF7` = `2.38:1` fails all; `#C9A227` on `#523E28` = `4.18:1` symbol/large text only).
4. 1-to-9 Symbol Concepts: `1, 3, 5, 6, 8, 9` approved; `2, 4, 7` strictly `"Not configured"`.
5. `APPROVED`-only archetype parity with `archetype_engine.py`; draft rules excluded (`NOT_CONFIGURED`).
6. Regional colour context (`INDIA` vs `INTERNATIONAL`), perception rules, Free-Scan verdict matrix,
   mandatory `evidence_label` enum, and standalone `pdf_service/` Docker context execution.
"""

import pathlib
import subprocess
import sys
import unittest

from app.engine.archetype_engine import DEFAULT_RULE_REGISTRY
from app.engine.business_taxonomy import TAXONOMY_TREE
from app.engine.number_characteristics_registry import NUMBER_REGISTRY
from app.logo_intelligence.rulebook_v1 import (
    EvidenceLabel,
    LogoRulebookV1,
    VALID_EVIDENCE_LABELS,
    calculate_contrast_ratio_hex,
    classify_hex_colour_family,
    compute_free_scan_verdict,
    evaluate_contrast_gate,
    get_rulebook_v1,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestLogoRulebookV1(unittest.TestCase):

    def setUp(self) -> None:
        self.rb = get_rulebook_v1()

    def test_single_digit_1_to_9_registry_parity_and_immutability(self):
        for n in range(1, 10):
            prof = self.rb.get_single_digit_numerology_rule(n)
            orig = NUMBER_REGISTRY[n]
            self.assertEqual(prof["root_number"], n)
            self.assertEqual(prof["planet"], orig["planet"])
            self.assertEqual(prof["friendly_numbers"], orig["friendly_numbers"])
            self.assertEqual(prof["neutral_numbers"], orig["neutral_numbers"])
            self.assertEqual(prof["enemy_numbers"], orig["enemy_numbers"])
            self.assertEqual(prof["favourable_colours"], orig["favourable_colours"])
            self.assertEqual(prof["colours_to_avoid"], orig["colours_to_avoid"])
            self.assertEqual(prof["evidence_label"], EvidenceLabel.TRADITIONAL_RULE.value)

            # Mutating output must never mutate NUMBER_REGISTRY
            prof["friendly_numbers"].append(999)
            self.assertNotIn(999, NUMBER_REGISTRY[n]["friendly_numbers"])

        # Master numbers, zero, >9, and booleans must be rejected
        for invalid in (0, 10, 11, 22, 33, -1, True, "8"):
            with self.assertRaises(ValueError):
                self.rb.get_single_digit_numerology_rule(invalid)  # type: ignore[arg-type]

    def test_d6_client_palettes_follow_client_numerology_tables_no_blanket_navy_or_black_ban(self):
        # Policy explicitly enabled
        policy = self.rb.raw_data["client_palette_policy"]
        self.assertTrue(policy["allow_client_navy_and_black_when_chart_supports"])
        self.assertFalse(policy["ui_chrome_restriction_applies_to_client_logos"])

        # Root 8 (Saturn): Navy, Dark Blue, Charcoal, Steel Grey, and Mindful Black are FAVOURABLE
        for hex_code in ("#1E3A8A", "#1B365D", "#2F353B", "#4A5568", "#141414", "#000000"):
            res = self.rb.check_colour_against_root(hex_code, 8)
            self.assertEqual(res["alignment"], "FAVOURABLE", f"Expected {hex_code} favourable for Root 8, got {res}")
            self.assertFalse(res["is_avoided_colour"])
            self.assertTrue(res["is_favourable_colour"])

        # Root 8 (Saturn): Pure Golden Yellow (#C9A227, #FFD700) and Bright Red (#DC2626) are AVOIDED
        for bad_hex in ("#C9A227", "#FFD700", "#DC2626"):
            res = self.rb.check_colour_against_root(bad_hex, 8)
            self.assertEqual(res["alignment"], "AVOID", f"Expected {bad_hex} avoided for Root 8, got {res}")
            self.assertTrue(res["is_avoided_colour"])

        # Root 1 (Sun): Gold is FAVOURABLE, while Black / Dark Navy are AVOIDED by Root 1's own table
        self.assertEqual(self.rb.check_colour_against_root("#C9A227", 1)["alignment"], "FAVOURABLE")
        self.assertEqual(self.rb.check_colour_against_root("#8B6914", 1)["alignment"], "FAVOURABLE")
        self.assertEqual(self.rb.check_colour_against_root("#000000", 1)["alignment"], "AVOID")
        self.assertEqual(self.rb.check_colour_against_root("#0F172A", 1)["alignment"], "AVOID")

    def test_measured_contrast_gates_including_gold_on_sandalwood_4_18(self):
        # #C9A227 on #FFFDF7 -> 2.38:1 -> fails symbol, large_text, and small_text
        for usage in ("symbol", "large_text", "small_text"):
            res = evaluate_contrast_gate("#C9A227", "#FFFDF7", usage=usage)
            self.assertEqual(res["measured_ratio"], 2.38)
            self.assertFalse(res["passed"])
            self.assertEqual(res["evidence_label"], EvidenceLabel.MEASURED.value)

        # #C9A227 on #523E28 -> 4.18:1 -> passes symbol & large_text ONLY; fails small_text
        sym_res = evaluate_contrast_gate("#C9A227", "#523E28", usage="symbol")
        lg_res = evaluate_contrast_gate("#C9A227", "#523E28", usage="large_text")
        sm_res = evaluate_contrast_gate("#C9A227", "#523E28", usage="small_text")
        self.assertEqual(sym_res["measured_ratio"], 4.18)
        self.assertTrue(sym_res["passed"])
        self.assertTrue(lg_res["passed"])
        self.assertFalse(sm_res["passed"])
        self.assertTrue(sm_res["symbol_and_large_text_only"])

        # #8B6914 on #FFFDF7 (5.00:1) & #FFFDF7 on #523E28 (9.93:1) pass small_text
        self.assertTrue(evaluate_contrast_gate("#8B6914", "#FFFDF7", usage="small_text")["passed"])
        self.assertAlmostEqual(calculate_contrast_ratio_hex("#FFFDF7", "#523E28"), 9.93, places=2)
        self.assertTrue(evaluate_contrast_gate("#FFFDF7", "#523E28", usage="small_text")["passed"])

    def test_symbol_concepts_1_to_9_with_2_4_7_not_configured(self):
        expected_approved = {
            1: "solar_crest",
            3: "golden_triangle",
            5: "mercury_caduceus",
            6: "sacred_lotus",
            8: "ascending_peak",
            9: "mars_shield",
        }
        for root, sym_id in expected_approved.items():
            entry = self.rb.get_symbol_concept_for_root(root)
            self.assertEqual(entry["status"], "APPROVED")
            self.assertEqual(entry["symbol_id"], sym_id)
            self.assertEqual(entry["evidence_label"], EvidenceLabel.TRADITIONAL_RULE.value)

        for unconfigured_root in (2, 4, 7):
            entry = self.rb.get_symbol_concept_for_root(unconfigured_root)
            self.assertEqual(entry["status"], "NOT_CONFIGURED")
            self.assertEqual(entry["display_status"], "Not configured")
            self.assertIsNone(entry["symbol_id"])
            self.assertEqual(entry["evidence_label"], EvidenceLabel.NOT_CONFIGURED.value)

    def test_approved_archetypes_parity_and_draft_exclusion(self):
        engine_approved = {
            rid: rule
            for rid, rule in DEFAULT_RULE_REGISTRY.items()
            if rule.is_active_for_production()
        }
        json_approved = self.rb.raw_data["approved_business_archetype_rules"]
        self.assertEqual(set(engine_approved.keys()), set(json_approved.keys()))
        for rid, eng_rule in engine_approved.items():
            self.assertEqual(json_approved[rid]["associated_number"], eng_rule.associated_number)
            self.assertEqual(json_approved[rid]["archetype"], eng_rule.archetype)

        # Draft rules must never be active; querying them returns NOT_CONFIGURED
        for draft_id in (
            "SPORTS_ARCHETYPE_SATURN_8",
            "SPORTS_ARCHETYPE_KETU_7",
            "BUSINESS_ARCHETYPE_SATURN_001",
            "BUSINESS_ARCHETYPE_RAHU_001",
        ):
            st = self.rb.get_archetype_rule_status(draft_id)
            self.assertEqual(st["status"], "NOT_CONFIGURED")
            self.assertEqual(st["evidence_label"], EvidenceLabel.NOT_CONFIGURED.value)

        # Every TAXONOMY_TREE category is covered in Layer 1 category norms
        for tax_cat in TAXONOMY_TREE:
            prof = self.rb.get_layer1_category_profile(tax_cat, region="INDIA")
            self.assertEqual(prof["status"], "RESOLVED", f"Category {tax_cat} failed to resolve")
            self.assertIn(prof["evidence_label"], VALID_EVIDENCE_LABELS)

        # Unknown category returns INSUFFICIENT_EVIDENCE
        unk = self.rb.get_layer1_category_profile("UNKNOWN", region="INDIA")
        self.assertEqual(unk["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(unk["evidence_label"], EvidenceLabel.NOT_CONFIGURED.value)

    def test_regional_context_perception_guidance_and_verdict_rule(self):
        india_food = self.rb.get_layer1_category_profile("hospitality_food", region="INDIA")
        intl_food = self.rb.get_layer1_category_profile("hospitality_food", region="INTERNATIONAL")
        self.assertTrue(india_food["pure_black_category_caution"])
        self.assertFalse(intl_food["pure_black_category_caution"])

        guidance = self.rb.derive_shape_and_lightness_guidance(
            ["care", "gentle", "modern"], price_position="mid"
        )
        self.assertEqual(guidance["shape_guidance"]["recommended_shape_family"], "circular_curved")
        self.assertEqual(guidance["lightness_guidance"]["recommended_lightness"], "light_or_medium_value_range")
        self.assertEqual(guidance["shape_guidance"]["evidence_label"], EvidenceLabel.PUBLISHED_RESEARCH.value)

        # Confirmed three-state verdict matrix
        self.assertEqual(compute_free_scan_verdict(True, False)["verdict"], "Aligned")
        self.assertEqual(compute_free_scan_verdict(False, False)["verdict"], "Partly aligned")
        self.assertEqual(compute_free_scan_verdict(True, True)["verdict"], "Partly aligned")
        self.assertEqual(compute_free_scan_verdict(False, True)["verdict"], "Not aligned")

    def test_pdf_service_mirror_byte_identity_and_isolated_import(self):
        pairs = [
            ("data/logo_rules_v1.json", "pdf_service/data/logo_rules_v1.json"),
            ("app/logo_intelligence/__init__.py", "pdf_service/app/logo_intelligence/__init__.py"),
            ("app/logo_intelligence/rulebook_v1.py", "pdf_service/app/logo_intelligence/rulebook_v1.py"),
        ]
        for src_rel, dst_rel in pairs:
            src_bytes = (ROOT / src_rel).read_bytes().replace(b"\r\n", b"\n")
            dst_bytes = (ROOT / dst_rel).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(src_bytes, dst_bytes, f"Mirror drift between {src_rel} and {dst_rel}")

        # Run rulebook inside isolated `pdf_service/` working directory (Render Docker context)
        probe = (
            "import os, sys; sys.path.insert(0, os.getcwd()); "
            "from app.logo_intelligence.rulebook_v1 import get_rulebook_v1, evaluate_contrast_gate; "
            "rb = get_rulebook_v1(); "
            "assert rb.get_symbol_concept_for_root(2)['status'] == 'NOT_CONFIGURED'; "
            "assert rb.check_colour_against_root('#1E3A8A', 8)['alignment'] == 'FAVOURABLE'; "
            "assert evaluate_contrast_gate('#C9A227', '#523E28', 'symbol')['passed'] is True; "
            "assert evaluate_contrast_gate('#C9A227', '#523E28', 'small_text')['passed'] is False; "
            "print('PDF_SERVICE_ISOLATED_OK')"
        )
        proc = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=str(ROOT / "pdf_service"),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=20,
        )
        self.assertIn("PDF_SERVICE_ISOLATED_OK", proc.stdout)


if __name__ == "__main__":
    unittest.main()
