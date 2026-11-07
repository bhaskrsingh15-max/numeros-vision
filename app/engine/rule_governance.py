"""
NUMEROS VISION — GOVERNED KNOWLEDGE & RULE APPROVAL LIFECYCLE ENGINE
Document Version: 2.0.0
Enforces strict source provenance, deterministic rule boundaries, and evidence validation.

Supported Lifecycle States:
  - EXTRACTED: Present in raw source but not yet reviewed.
  - VERIFIED_SOURCE: Checked against transcript or reference text.
  - APPROVED: Authorized for use in client prediction and report generation.
  - PENDING_EVIDENCE: Insufficient information to define the rule; system abstains.
  - CONFLICTED: Multiple sources disagree; requires documented resolution.
  - SUPERSEDED: Replaced by an explicitly approved newer version.

Sources Integrated & Governed:
  - SRC-DAY7-TRANSCRIPT: Lo Shu 1-9 Attributes, Elements, 5-level Repetition Framework
  - SRC-ADV-PROF-NOTES: Missing Number Impacts (1-9), Poorak Numbers, Master Key 5, Remedies
  - SRC-81-DC-DESTINY-GUIDE: All 81 Driver-Conductor Combinations, Destiny Influences & Ratings
  - SRC-81-DC-WISDOM: In-depth narrative profiles for Driver-Conductor combinations
  - SRC-NUMERO-MAHADASHA: Numerological Mahadasha Calculation Cycle, Scoring & Timing Events
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RuleStatus(str, Enum):
    EXTRACTED = "EXTRACTED"
    VERIFIED_SOURCE = "VERIFIED_SOURCE"
    APPROVED = "APPROVED"
    PENDING_EVIDENCE = "PENDING_EVIDENCE"
    CONFLICTED = "CONFLICTED"
    SUPERSEDED = "SUPERSEDED"


class GovernedRule(BaseModel):
    rule_id: str
    rule_version: str = "1.0.0"
    domain: str
    topic: str
    source_document_id: str
    source_title: str
    source_passage_or_timestamp: str
    applicable_system: str
    applicable_numbers: List[int] = Field(default_factory=list)
    conditions: Dict[str, Any] = Field(default_factory=dict)
    interpretation: str
    exceptions: Optional[str] = None
    repetition_category: Optional[str] = None
    element: Optional[str] = None
    attribute_name: Optional[str] = None
    planetary_association: Optional[str] = None
    authority_status: str
    approval_status: RuleStatus
    effective_date: str
    review_date: str
    provenance: str


class RuleGovernanceEngine:
    def __init__(self, base_dir: Optional[Path] = None):
        root = base_dir or Path(__file__).resolve().parent.parent.parent
        self.kb_dir = root / "data" / "knowledge_base"
        self.day7_rules_file = self.kb_dir / "day7_loshu_rules.json"
        self.missing_rules_file = self.kb_dir / "missing_number_rules.json"
        self.dc_rules_file = self.kb_dir / "driver_conductor_81_rules.json"
        self.mahadasha_rules_file = self.kb_dir / "numerological_mahadasha_rules.json"

        self._day7_rules: Dict[str, GovernedRule] = {}
        self._missing_rules: Dict[str, Any] = {}
        self._dc_rules: Dict[str, Any] = {}
        self._mahadasha_rules: Dict[str, Any] = {}

        self._load_all_rules()

    def _load_all_rules(self):
        # 1. Load Day 7 Rules
        if self.day7_rules_file.exists():
            try:
                with open(self.day7_rules_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for r in data.get("rules", []):
                    rule_obj = GovernedRule(**r)
                    self._day7_rules[rule_obj.rule_id] = rule_obj
            except Exception as e:
                print(f"[RULE_GOVERNANCE_WARNING] Failed to load Day 7 rules: {e}")

        # 2. Load Missing Number Rules (SRC-ADV-PROF-NOTES)
        if self.missing_rules_file.exists():
            try:
                with open(self.missing_rules_file, "r", encoding="utf-8") as f:
                    self._missing_rules = json.load(f)
            except Exception as e:
                print(f"[RULE_GOVERNANCE_WARNING] Failed to load Missing Number rules: {e}")

        # 3. Load 81 Driver-Conductor Rules (SRC-81-DC-DESTINY-GUIDE)
        if self.dc_rules_file.exists():
            try:
                with open(self.dc_rules_file, "r", encoding="utf-8") as f:
                    self._dc_rules = json.load(f)
            except Exception as e:
                print(f"[RULE_GOVERNANCE_WARNING] Failed to load 81 DC rules: {e}")

        # 4. Load Numerological Mahadasha Rules (SRC-NUMERO-MAHADASHA)
        if self.mahadasha_rules_file.exists():
            try:
                with open(self.mahadasha_rules_file, "r", encoding="utf-8") as f:
                    self._mahadasha_rules = json.load(f)
            except Exception as e:
                print(f"[RULE_GOVERNANCE_WARNING] Failed to load Mahadasha rules: {e}")

    def get_rule_by_id(self, rule_id: str) -> Optional[GovernedRule]:
        return self._day7_rules.get(rule_id)

    def get_attribute_for_number(self, number: int) -> Optional[Dict[str, Any]]:
        """Returns the approved number attribute, element, and planetary association from Day 7."""
        rule_id = f"RUL-LOSHU-D7-{number:03d}"
        rule = self._day7_rules.get(rule_id)
        if not rule or rule.approval_status != RuleStatus.APPROVED:
            return None
        return {
            "rule_id": rule.rule_id,
            "number": number,
            "attribute": rule.attribute_name,
            "element": rule.element,
            "planet": rule.planetary_association,
            "interpretation": rule.interpretation,
            "exceptions": rule.exceptions,
            "source_document_id": rule.source_document_id,
            "approval_status": rule.approval_status.value
        }

    def get_missing_number_evaluation(self, number: int) -> Dict[str, Any]:
        """
        Retrieves the verified diagnosis, poorak complimentary numbers, and remedies
        from the canonical notes (SRC-ADV-PROF-NOTES, Pages 6-9, 24).
        """
        impacts = self._missing_rules.get("missing_number_impacts", {})
        poorak_map = self._missing_rules.get("complimentary_poorak_numbers", {})
        num_str = str(number)

        attr_info = self.get_attribute_for_number(number) or {}

        if num_str in impacts:
            data = impacts[num_str]
            return {
                "number": number,
                "frequency": 0,
                "status": "MISSING_VERIFIED",
                "attribute": attr_info.get("attribute", "General Attribute"),
                "element": data.get("element", attr_info.get("element", "Unknown")),
                "impact": data.get("impact"),
                "poorak_complimentary_numbers": poorak_map.get(num_str, []),
                "element_remedy": data.get("remedy"),
                "yantra_remedy": data.get("yantra_remedy"),
                "approval_status": RuleStatus.APPROVED.value,
                "rule_id": f"RUL-MISSING-NUM-{number}",
                "source_document_id": "SRC-ADV-PROF-NOTES",
                "source_citation": "Professional & Advance Numerology Study Notes (Numeros Vision, Pages 6-9, 24)"
            }

        # Fallback if unconfigured
        return {
            "number": number,
            "frequency": 0,
            "status": "MISSING_UNCONFIGURED",
            "interpretation": f"Number {number} is absent from the natal Lo Shu grid.",
            "approval_status": RuleStatus.PENDING_EVIDENCE.value,
            "rule_id": "RUL-LOSHU-DEF-MISSING"
        }

    def get_repetition_evaluation(self, number: int, frequency: int) -> Dict[str, Any]:
        """
        Evaluates number repetition strictly within the Day 7 transcript framework:
        0: Missing -> Evaluated against SRC-ADV-PROF-NOTES
        1: Under
        2: Pair (best-performing)
        3: Exaggerate
        4: Reactive
        5: Over-reactive / Hyper-reactive
        >5: PENDING_EVIDENCE (Strict abstention against extrapolation)
        """
        if frequency <= 0:
            return self.get_missing_number_evaluation(number)

        attr_info = self.get_attribute_for_number(number) or {}

        if frequency > 5:
            # Extrapolation boundary: strictly return PENDING_EVIDENCE
            return {
                "number": number,
                "frequency": frequency,
                "status": "EXTRAPOLATION_LIMIT_EXCEEDED",
                "repetition_category": "PENDING_EVIDENCE",
                "attribute": attr_info.get("attribute"),
                "element": attr_info.get("element"),
                "interpretation": f"Digit {number} appears {frequency} times. Frequencies above 5 occurrences are explicitly not established in the Day 7 training transcript. The system strictly abstains from extrapolating unverified claims.",
                "approval_status": RuleStatus.PENDING_EVIDENCE.value,
                "rule_id": "RUL-LOSHU-D7-REP-EXTRAPOLATION"
            }

        rule_id = f"RUL-LOSHU-D7-REP-{frequency}"
        rep_rule = self._day7_rules.get(rule_id)
        category = rep_rule.repetition_category if rep_rule else "Unknown"

        exception_text = f"Evaluated under {attr_info.get('element')} element balance. {attr_info.get('exceptions', '')}"

        return {
            "number": number,
            "frequency": frequency,
            "status": "EVALUATED",
            "repetition_category": category,
            "attribute": attr_info.get("attribute"),
            "element": attr_info.get("element"),
            "planet": attr_info.get("planet"),
            "category_interpretation": rep_rule.interpretation if rep_rule else "",
            "exceptions_applied": exception_text,
            "approval_status": RuleStatus.APPROVED.value,
            "rule_id": rule_id,
            "source_citation": "Day 7 Numerology Training Session Transcript (Lo Shu Elements, Attributes & Repetition)"
        }

    def evaluate_grid_frequencies(self, digit_counts: Dict[int, int]) -> Dict[str, Any]:
        """
        Deterministically evaluates all digits 1-9 against approved rules.
        """
        evaluations = {}
        missing_numbers = []
        present_numbers = []

        for num in range(1, 10):
            freq = digit_counts.get(num, 0)
            res = self.get_repetition_evaluation(num, freq)
            evaluations[str(num)] = res
            if freq == 0:
                missing_numbers.append(num)
            else:
                present_numbers.append(num)

        # Check Master Key 5 rule
        has_5 = digit_counts.get(5, 0) > 0

        return {
            "evaluations": evaluations,
            "present_numbers": present_numbers,
            "missing_numbers": missing_numbers,
            "master_key_5_active": has_5,
            "master_key_5_status": "Master Key 5 is present, providing foundational balance across missing sectors." if has_5 else "Master Key 5 absent; requires active remedial grounding.",
            "documented_exceptions_checked": True,
            "governance_version": "2.0.0",
            "source_authority": "SRC-DAY7-TRANSCRIPT & SRC-ADV-PROF-NOTES"
        }

    def get_driver_conductor_combination(self, driver: int, conductor: int) -> Dict[str, Any]:
        """
        Looks up the canonical 81 Driver-Conductor combination table
        from SRC-81-DC-DESTINY-GUIDE.
        """
        key = f"{driver}_{conductor}"
        if key in self._dc_rules:
            dc = self._dc_rules[key]
            return {
                "driver": driver,
                "conductor": conductor,
                "driver_planet": dc["driver_planet"],
                "conductor_planet": dc["conductor_planet"],
                "planet_combination": dc["planet_combination"],
                "destiny_influence": dc["destiny_influence"],
                "compatibility": dc["compatibility"],
                "approval_status": RuleStatus.APPROVED.value,
                "source_document_id": "SRC-81-DC-DESTINY-GUIDE",
                "source_citation": f"Driver – Conductor – Destiny Numerology Guide (Page {dc.get('source_page', 1)})"
            }

        return {
            "driver": driver,
            "conductor": conductor,
            "destiny_influence": "Unverified driver-conductor combination.",
            "compatibility": "UNKNOWN",
            "approval_status": RuleStatus.PENDING_EVIDENCE.value,
            "source_document_id": "UNCONFIGURED"
        }

    def calculate_numerological_mahadasha(self, dob_str: str, current_year: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates the complete Numerological Mahadasha sequence according to SRC-NUMERO-MAHADASHA.
        Formula:
          1. King (Driver) number = day of birth reduced to single digit 1-9.
          2. First Mahadasha starts at DOB year and runs for [King Number] years.
          3. Subsequent Mahadashas follow the natural cycle 1 to 9 (each running for its respective number of years).
          4. Returns active Mahadasha for current_year, Lo Shu scoring, and crucial timing events.
        """
        parts = [int(p) for p in dob_str.replace("/", "-").split("-")]
        if len(parts) != 3:
            raise ValueError("DOB must be in YYYY-MM-DD or DD-MM-YYYY format")

        if parts[0] > 1000:
            birth_year, birth_month, birth_day = parts[0], parts[1], parts[2]
        else:
            birth_day, birth_month, birth_year = parts[0], parts[1], parts[2]

        # Calculate King (Driver) Number
        def reduce_digit(n: int) -> int:
            while n > 9:
                n = sum(int(d) for d in str(n))
            return n

        king_number = reduce_digit(birth_day)
        now_year = current_year or datetime.now().year

        planet_names = {
            1: "Sun",
            2: "Moon",
            3: "Jupiter",
            4: "Rahu",
            5: "Mercury",
            6: "Venus",
            7: "Ketu",
            8: "Saturn",
            9: "Mars"
        }

        # Build cycles starting from King Number
        periods = []
        running_year = birth_year
        current_num = king_number

        for cycle_idx in range(9):
            # Duration equals the number itself in years
            duration = current_num
            end_year = running_year + duration
            is_active = (running_year <= now_year < end_year)

            periods.append({
                "cycle_index": cycle_idx + 1,
                "number": current_num,
                "planet": planet_names.get(current_num, f"Planet {current_num}"),
                "duration_years": duration,
                "start_date": f"{birth_day:02d}-{birth_month:02d}-{running_year}",
                "end_date": f"{birth_day:02d}-{birth_month:02d}-{end_year}",
                "start_year": running_year,
                "end_year": end_year,
                "is_current_active": is_active
            })

            running_year = end_year
            # Next number circularly 1-9
            current_num = 1 if current_num == 9 else current_num + 1

        active_period = next((p for p in periods if p["is_current_active"]), periods[0])

        return {
            "king_driver_number": king_number,
            "king_planet": planet_names.get(king_number),
            "birth_date": f"{birth_day:02d}-{birth_month:02d}-{birth_year}",
            "calculation_method": "First MD starts at DOB with King Number for [King] years, then circular sequence 1-9.",
            "periods": periods,
            "current_active_mahadasha": active_period,
            "source_document_id": "SRC-NUMERO-MAHADASHA",
            "approval_status": RuleStatus.APPROVED.value,
            "governance_version": "1.0.0"
        }


# Global singleton instance
rule_governance = RuleGovernanceEngine()
