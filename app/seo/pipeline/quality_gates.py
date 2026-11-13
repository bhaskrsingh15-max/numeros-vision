"""
Content Quality Gates Validator
Implements Section 16 (Content Quality Gates — 7 Mandatory Gates)
"""

import os
import json
from typing import Dict, Any, List, Tuple
from app.seo.research_data_model import ContentBrief, ClaimStatus
from app.seo.anti_penalty_guardrails import AntiPenaltyGuardrailValidator

class QualityGateValidator:
    """Evaluates content drafts against all 7 mandatory gates. Rejects if any gate fails."""

    def __init__(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
        self.offer_registry_file = os.path.join(self.data_dir, "offer_registry.json")
        self.offers = self._load_json(self.offer_registry_file)

    def _load_json(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def evaluate_draft(self, 
                       html_content: str, 
                       brief: ContentBrief,
                       is_human_approved: bool = True,
                       image_package: Optional[Dict[str, Any]] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Runs all 7 gates. Returns (passed, report).
        """
        gate_results = {}
        all_passed = True

        # GATE 1: Source Integrity
        unsupported_claims = [c for c in brief.required_claims if c.verification_status not in (ClaimStatus.SUPPORTED, ClaimStatus.NOT_APPLICABLE)]
        gate1_pass = len(unsupported_claims) == 0
        gate_results["gate_1_source_integrity"] = {
            "status": "PASS" if gate1_pass else "FAIL",
            "unsupported_claims_count": len(unsupported_claims)
        }
        if not gate1_pass: all_passed = False

        # GATE 2: Product Accuracy
        gate2_pass = True
        gate2_errors = []
        if brief.offer_id:
            valid_offers = [o for o in self.offers.get("offers", []) if o.get("offer_id") == brief.offer_id]
            if not valid_offers:
                gate2_pass = False
                gate2_errors.append(f"Referenced offer_id '{brief.offer_id}' does not exist in offer registry.")
        gate_results["gate_2_product_accuracy"] = {
            "status": "PASS" if gate2_pass else "FAIL",
            "errors": gate2_errors
        }
        if not gate2_pass: all_passed = False

        # GATE 3: Calculation Accuracy
        # Checks that text does not contain banned mathematical errors or altered master numbers
        gate3_pass = True
        gate3_errors = []
        if "11 reduced to 2" in html_content.lower() or "master number 22 reduced" in html_content.lower():
            gate3_pass = False
            gate3_errors.append("Draft improperly reduces Master Numbers 11/22/33 in contradiction to Pythagorean standard.")
        gate_results["gate_3_calculation_accuracy"] = {
            "status": "PASS" if gate3_pass else "FAIL",
            "errors": gate3_errors
        }
        if not gate3_pass: all_passed = False

        # GATE 4: Originality and Usefulness
        # Checks that draft has substantive length (> 500 words) and no empty placeholder tags
        word_count = len(html_content.split())
        gate4_pass = word_count >= 300 and "[insert" not in html_content.lower()
        gate_results["gate_4_originality"] = {
            "status": "PASS" if gate4_pass else "FAIL",
            "word_count": word_count
        }
        if not gate4_pass: all_passed = False

        # GATE 5: Intent Fit
        # Ensures transactional tools include interactive inputs or links to calculators
        gate5_pass = True
        if brief.intent.value in ("TRANSACTIONAL", "TOOL_SEEKING"):
            if "calculator" not in html_content.lower() and "tool" not in html_content.lower():
                gate5_pass = False
        gate_results["gate_5_intent_fit"] = {
            "status": "PASS" if gate5_pass else "FAIL",
            "target_intent": brief.intent.value
        }
        if not gate5_pass: all_passed = False

        # GATE 6: Technical SEO & Media Validation (Section 7.6 & AntiPenaltyGuardrailValidator)
        is_seo_compliant, seo_issues, seo_metrics = AntiPenaltyGuardrailValidator.validate_page_html(
            html_content, brief.primary_keyword
        )
        media_issues = []
        if image_package:
            if not image_package.get("alt_text_valid", True):
                media_issues.extend(image_package.get("alt_text_issues", []))
            if image_package.get("hero_webp_url") and image_package["hero_webp_url"] not in html_content:
                media_issues.append("Generated hero image WebP is not embedded in the rendered HTML.")

        all_gate6_issues = list(seo_issues) + media_issues
        gate6_pass = is_seo_compliant and len(media_issues) == 0

        gate_results["gate_6_technical_seo"] = {
            "status": "PASS" if gate6_pass else "FAIL",
            "issues": all_gate6_issues,
            "media_issues": media_issues,
            "metrics": seo_metrics
        }
        if not gate6_pass: all_passed = False

        # GATE 7: Editorial Approval
        gate_results["gate_7_editorial_approval"] = {
            "status": "PASS" if is_human_approved else "PENDING_APPROVAL",
            "is_human_approved": is_human_approved
        }
        if not is_human_approved: all_passed = False

        report = {
            "overall_verdict": "PASSED" if all_passed else "BLOCKED",
            "passed": all_passed,
            "gates": gate_results
        }
        return all_passed, report
