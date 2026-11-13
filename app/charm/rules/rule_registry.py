"""
app/charm/rules/rule_registry.py
=================================
Master Rule Registry & Lifecycle Governance for Charm AI.
Complies with Section 4.3 of Master Specification v2.0.
"""

import hashlib
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class RuleLocator(BaseModel):
    type: str = Field("page", description="page, section, folio, or timestamp")
    start: str = Field(..., description="Starting locator reference")
    end: str = Field(..., description="Ending locator reference")

class RuleRecord(BaseModel):
    rule_id: str
    method_id: str = Field(..., description="NUMEROLOGY_DASHA, KP_ASTROLOGY, VEDIC_ASTROLOGY, BNN_NADI, LAL_KITAB")
    rule_name: str
    rule_text_normalized: str
    source_id: str
    locator: RuleLocator
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    required_facts: List[str] = Field(default_factory=list)
    event_types: List[str] = Field(default_factory=list)
    timing_effect: str
    exceptions: List[str] = Field(default_factory=list)
    conflict_ids: List[str] = Field(default_factory=list)
    review_status: str = Field("UNVERIFIED", description="UNVERIFIED, APPROVED, CONFLICTED, DISABLED")
    reviewer_id: Optional[str] = None
    rule_version: str = "1.0"
    test_case_ids: List[str] = Field(default_factory=list)
    rule_hash: str = ""

    def is_production_eligible(self) -> bool:
        return (
            self.review_status == "APPROVED"
            and bool(self.source_id)
            and bool(self.locator.start)
            and len(self.conflict_ids) == 0
        )

class RuleRegistry:
    def __init__(self):
        self._rules: Dict[str, RuleRecord] = {}
        self._register_canonical_rules()

    def register(self, rule: RuleRecord) -> RuleRecord:
        raw = f"{rule.rule_id}:{rule.method_id}:{rule.rule_text_normalized}:{rule.source_id}:{rule.rule_version}"
        rule.rule_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
        self._rules[rule.rule_id] = rule
        return rule

    def get_rule(self, rule_id: str) -> Optional[RuleRecord]:
        return self._rules.get(rule_id)

    def get_rules_by_method(self, method_id: str, production_only: bool = True) -> List[RuleRecord]:
        res = [r for r in self._rules.values() if r.method_id == method_id]
        if production_only:
            res = [r for r in res if r.is_production_eligible()]
        return res

    def get_rules_for_event(self, event_type: str, method_id: Optional[str] = None) -> List[RuleRecord]:
        res = []
        for r in self._rules.values():
            if not r.is_production_eligible():
                continue
            if method_id and r.method_id != method_id:
                continue
            if event_type in r.event_types or "all" in r.event_types:
                res.append(r)
        return res

    def _register_canonical_rules(self):
        # 1. Numerology Dasha Mahadasha Rule
        self.register(RuleRecord(
            rule_id="RULE-ND-MD-001",
            method_id="NUMEROLOGY_DASHA",
            rule_name="9-Year Mahadasha Planetary Cycle",
            rule_text_normalized="Mahadasha progresses in 9-year cyclic intervals anchored by the natal Driver number and sequential planetary rulers.",
            source_id="SRC-NV-005",
            locator=RuleLocator(type="section", start="Section 4.1", end="Section 4.4"),
            conditions=[{"field": "driver", "operator": "in", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9]}],
            required_facts=["driver", "chronological_age"],
            event_types=["career", "wealth", "marriage", "health", "property", "general"],
            timing_effect="Defines the overarching 9-year planetary ruler and macro developmental climate.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-ND-001"]
        ))

        # 2. Numerology Dasha Antardasha Rule
        self.register(RuleRecord(
            rule_id="RULE-ND-AD-001",
            method_id="NUMEROLOGY_DASHA",
            rule_name="Annual Antardasha Sub-Period Sequence",
            rule_text_normalized="Antardasha divides the 9-year Mahadasha into nine 1-year annual sub-periods, modulating the active Personal Year frequency.",
            source_id="SRC-NV-005",
            locator=RuleLocator(type="section", start="Section 4.5", end="Section 4.8"),
            conditions=[{"field": "mahadasha", "operator": "exists", "values": []}],
            required_facts=["mahadasha", "current_age"],
            event_types=["career", "wealth", "marriage", "health", "property", "general"],
            timing_effect="Modulates annual events and triggers breakthrough or consolidation phases.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-ND-002"]
        ))

        # 3. Numerology Dasha Pratyantardasha Rule
        self.register(RuleRecord(
            rule_id="RULE-ND-PD-001",
            method_id="NUMEROLOGY_DASHA",
            rule_name="Multi-Month Pratyantardasha Sub-Sub Window",
            rule_text_normalized="Pratyantardasha divides each 1-year Antardasha into nine 40-day proportionate sub-sub intervals to isolate acute event timing.",
            source_id="SRC-NV-003",
            locator=RuleLocator(type="page", start="Folio 42", end="Folio 46"),
            conditions=[{"field": "antardasha", "operator": "exists", "values": []}],
            required_facts=["antardasha", "target_date"],
            event_types=["career", "wealth", "marriage", "health", "property"],
            timing_effect="Pinpoints acute 40-day execution horizons within the annual sub-period.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-ND-003"]
        ))

        # 4. KP Sub-Lord Career Significator Rule
        self.register(RuleRecord(
            rule_id="RULE-KP-CAREER-001",
            method_id="KP_ASTROLOGY",
            rule_name="KP 10th Cusp Sub-Lord Career Indicator",
            rule_text_normalized="When the 10th cuspal sub-lord signifies houses 2, 6, 10, or 11, career breakthroughs and professional appointments are strongly supported.",
            source_id="SRC-NV-004",
            locator=RuleLocator(type="section", start="Cuspal Sub-Lord Matrix", end="Page 88"),
            conditions=[{"field": "sublord_significators", "operator": "intersects", "values": [2, 6, 10, 11]}],
            required_facts=["tenth_sublord", "house_significations"],
            event_types=["career"],
            timing_effect="Corroborates active professional promotion or job offer during corresponding Dasha/Transit.",
            exceptions=["If sub-lord is afflicted by 8 or 12 without 11 relief, results in operational delays"],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-KP-001"]
        ))

        # 5. Vedic Parashari Transit Yoga Rule
        self.register(RuleRecord(
            rule_id="RULE-VEDIC-TRANSIT-001",
            method_id="VEDIC_ASTROLOGY",
            rule_name="Jupiter Gochar Transit Blessing",
            rule_text_normalized="Jupiter transit over natal 1st, 5th, 9th, or 11th houses establishes a protective Dhana/Dharma expansion window.",
            source_id="SRC-NV-001",
            locator=RuleLocator(type="section", start="Gochar Chapters", end="Folio 104"),
            conditions=[{"field": "jupiter_transit_house", "operator": "in", "values": [1, 5, 9, 11]}],
            required_facts=["jupiter_transit_longitude", "natal_moon_sign"],
            event_types=["career", "wealth", "marriage", "education"],
            timing_effect="Expands fortune, ethical standing, and milestone success.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-VED-001"]
        ))

        # 6. BNN Karaka Conjunction Rule
        self.register(RuleRecord(
            rule_id="RULE-BNN-KARAKA-001",
            method_id="BNN_NADI",
            rule_name="Saturn-Jupiter Karma-Dharma Axis",
            rule_text_normalized="Conjunction or 1-5-9 trinal trine between Saturn (Karma) and Jupiter (Jeeva) initiates high institutional respect and ethical professional compounding.",
            source_id="SRC-NV-007",
            locator=RuleLocator(type="section", start="Video 2 Saturn Combinations", end="Timestamp 12:45"),
            conditions=[{"field": "saturn_jupiter_relation", "operator": "in", "values": ["conjunction", "trine"]}],
            required_facts=["saturn_position", "jupiter_position"],
            event_types=["career", "wealth"],
            timing_effect="Guarantees sustained professional foundation and societal recognition.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-BNN-001"]
        ))

        # 7. Quarantined Lal Kitab Masnooi Rule (DISABLED per Section 1.2)
        self.register(RuleRecord(
            rule_id="RULE-LK-MASNOOI-001",
            method_id="LAL_KITAB",
            rule_name="Lal Kitab Masnooi Alchemy (Unverified)",
            rule_text_normalized="Synthetic planetary pairs generate secondary planetary vibrations modifying destiny awakening ages.",
            source_id="SRC-NV-LK-UNVERIFIED",
            locator=RuleLocator(type="folio", start="Folio 12", end="Folio 14"),
            conditions=[],
            required_facts=[],
            event_types=["career", "general"],
            timing_effect="Speculative awakening age modulation.",
            exceptions=[],
            conflict_ids=["CONFLICT-LK-001"],
            review_status="DISABLED",
            reviewer_id=None,
            rule_version="0.1-DRAFT",
            test_case_ids=[]
        ))

        # 8. Western Pythagorean Numerology Rule
        self.register(RuleRecord(
            rule_id="RULE-PYTH-LP-001",
            method_id="PYTHAGOREAN_NUMEROLOGY",
            rule_name="Western Life Path Single-Digit Archetype",
            rule_text_normalized="Computes Life Path via full digit reduction strictly to a single digit 1-9 (no 11/22/33 retention) and identifies Karmic Debt compound numbers (13, 14, 16, 19).",
            source_id="SRC-NV-PYTH-001",
            locator=RuleLocator(type="section", start="Section 3.1", end="Section 3.5"),
            conditions=[{"field": "life_path_number", "operator": "in", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9]}],
            required_facts=["life_path_number", "karmic_debt"],
            event_types=["career", "wealth", "general"],
            timing_effect="Identifies structural purpose, master potentials, and karmic learning curves.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-PYTH-001"]
        ))

        # 9. Vedic Sankhya Shastra Rule
        self.register(RuleRecord(
            rule_id="RULE-VEDIC-NUM-001",
            method_id="VEDIC_NUMEROLOGY",
            rule_name="Driver-Conductor Dynamic Harmony Matrix",
            rule_text_normalized="Vedic Sankhya Shastra analyzes the mutual relationship between Mulank (Driver) and Bhagyank (Conductor) to assess internal synergy and life friction.",
            source_id="SRC-NV-SANKHYA-001",
            locator=RuleLocator(type="section", start="Chapter 2", end="Verse 14"),
            conditions=[{"field": "driver", "operator": "in", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9]}],
            required_facts=["driver", "conductor"],
            event_types=["career", "wealth", "marriage", "general"],
            timing_effect="Establishes baseline harmony and predicts ease or friction in executing personal decisions.",
            exceptions=[],
            conflict_ids=[],
            review_status="APPROVED",
            reviewer_id="Chief Astrological Officer",
            rule_version="1.0",
            test_case_ids=["TC-VNUM-001"]
        ))

rule_registry = RuleRegistry()
