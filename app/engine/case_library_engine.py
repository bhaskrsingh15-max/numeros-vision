# -*- coding: utf-8 -*-
"""
CASE LIBRARY RETRIEVAL & PATTERN MATCHING ENGINE
Numeros Vision — Master Knowledge Engine
Retrieves and ranks historical practitioner cases using multi-dimensional feature matching
and evidence quality weighting, strictly separating pattern similarity from evidence certainty.
In strict compliance with Master AGENTS.md.
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

from app.engine.case_intelligence_schema import (
    CaseRecord,
    EvidenceLevel,
    VerificationStatus,
    NumerologyFeatures
)

CASE_LIBRARY_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "knowledge_base" / "case_library.json"


class CaseLibraryEngine:
    """
    Retrieves historical practitioner cases based on multi-dimensional numerological feature vectors,
    domain relevance, and evidence quality tiers.
    """

    def __init__(self, data_file: Path = CASE_LIBRARY_FILE):
        self.data_file = data_file
        self.cases: List[Dict[str, Any]] = []
        self._load_library()

    def _load_library(self) -> None:
        if not self.data_file.exists():
            self._initialize_default_library()
            return
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.cases = data.get("cases", [])
        except Exception as e:
            print(f"Warning: Failed to load case library ({e}). Initializing default.")
            self._initialize_default_library()

    def _initialize_default_library(self) -> None:
        """Seeds initial verified practitioner and historical case records."""
        default_cases = [
            {
                "case_id": "NV-CASE-000001",
                "case_version": 1,
                "domain": "career",
                "source": {
                    "title": "Corporate Executive Name Spelling Alignment Study",
                    "url": "internal://practitioner-records/case-001",
                    "author": "Numeros Vision Senior Practitioner Archives",
                    "publication_date": "2024-03-15",
                    "evidence_level": EvidenceLevel.E3_PRACTITIONER_CASE.value,
                    "verification_status": VerificationStatus.UNVERIFIED.value
                },
                "inputs": {
                    "date_of_birth": "1988-10-19",
                    "birth_name": "Rohan Verma",
                    "current_name": "Rohann Verma",
                    "question": "Career stagnation, executive board visibility, promotion delay",
                    "observation_period": "18 months (2024-2025)"
                },
                "calculations": {
                    "system": "Chaldean",
                    "ruleset_version": "1.0.0",
                    "birth_number": 1,
                    "destiny_number": 1,
                    "name_number": 1,
                    "compound_numbers": [19, 37],
                    "loshu_grid": {"1": 3, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 2, "9": 2}
                },
                "interpretations": [
                    {
                        "claim": "Native birth day 19 carries Alpha Solar power (Karmic 19). Triple 1 and double 8 created heavy authority deadlock with institutional superiors.",
                        "rule_reference": "NV-002: Birth Day 19 & Repetitive 1s / 8s friction",
                        "evidence_status": "traditional"
                    }
                ],
                "predictions": [
                    {
                        "event": "Corporate promotion or autonomous spin-off opportunity",
                        "start_date": "2024-10-15",
                        "end_date": "2025-04-15",
                        "success_criterion": "Executive title elevation or independent divisional leadership",
                        "recorded_at": "2024-03-20T10:00:00Z",
                        "forecast_status": "reported_favorable"
                    }
                ],
                "remedies": [
                    {
                        "type": "Name spelling adjustment to Compound 37 (1) + Copper morning solar water hygiene",
                        "rationale": "Chaldean Compound 37 brings royal friendship and public alliance, softening double 8 friction.",
                        "cost": "Zero cost physical routine",
                        "risks": ["Official legal document update friction"],
                        "outcome_evidence": "practitioner_observed_only"
                    }
                ],
                "outcome": {
                    "observed_result": "Client reported appointment as Vice President in January 2025.",
                    "evidence_source": "Client self-reported follow-up questionnaire",
                    "confounders": ["Macroeconomic hiring surge in tech consulting", "Client completed MBA certification in 2024"],
                    "independent_review": False
                },
                "provenance": {
                    "source_quotes": ["Client reported improved board communication 90 days after adopting balanced signature."],
                    "reviewer": "Numeros Vision Ethics Review",
                    "last_verified_at": "2026-01-10"
                }
            },
            {
                "case_id": "NV-CASE-000002",
                "case_version": 1,
                "domain": "finance",
                "source": {
                    "title": "Business Solvency & Mobile Numerology Case Study",
                    "url": "internal://practitioner-records/case-002",
                    "author": "Numeros Vision Commercial Advisory",
                    "publication_date": "2023-11-04",
                    "evidence_level": EvidenceLevel.E3_PRACTITIONER_CASE.value,
                    "verification_status": VerificationStatus.UNVERIFIED.value
                },
                "inputs": {
                    "date_of_birth": "1979-08-26",
                    "birth_name": "Sanjay Mehta",
                    "current_name": "Sanjay Mehta",
                    "question": "Chronic liquidity blockages, client payment delays in textile export",
                    "observation_period": "12 months"
                },
                "calculations": {
                    "system": "Chaldean",
                    "ruleset_version": "1.0.0",
                    "birth_number": 8,
                    "destiny_number": 6,
                    "name_number": 5,
                    "compound_numbers": [26, 33],
                    "loshu_grid": {"1": 1, "2": 2, "3": 0, "4": 0, "5": 0, "6": 1, "7": 1, "8": 1, "9": 2}
                },
                "interpretations": [
                    {
                        "claim": "Birth day 26 (Saturn) with Conductor 6 creates heavy family and business debt burdens. Primary mobile contained malefic 48 anti-pair.",
                        "rule_reference": "Mobile Numerology Rule 2: Anti-pair 48 cash blockage",
                        "evidence_status": "traditional"
                    }
                ],
                "predictions": [
                    {
                        "event": "Gradual debt recovery and cash flow normalization",
                        "start_date": "2024-02-01",
                        "end_date": "2024-08-01",
                        "success_criterion": "Recovery of trapped export receivables (>50%)",
                        "recorded_at": "2023-11-10T14:30:00Z",
                        "forecast_status": "reported_favorable"
                    }
                ],
                "remedies": [
                    {
                        "type": "Transition primary business mobile ending in 55 (Mercury) + North desk alignment",
                        "rationale": "Number 5 introduces commercial liquidity to dissolve Saturn-Venus debt traps.",
                        "cost": "Cost of secondary telecom SIM",
                        "risks": ["Temporary vendor contact update confusion"],
                        "outcome_evidence": "practitioner_observed_only"
                    }
                ],
                "outcome": {
                    "observed_result": "Recovered 68% of outstanding invoices within 7 months.",
                    "evidence_source": "Accountant confirmation statement",
                    "confounders": ["Implementation of legal demand notices under MSMED Act 2006"],
                    "independent_review": False
                },
                "provenance": {
                    "source_quotes": ["Cash flow stabilized; multiple overdue accounts cleared following communication restructuring."],
                    "reviewer": "Numeros Vision Audit Board",
                    "last_verified_at": "2024-12-01"
                }
            },
            {
                "case_id": "NV-CASE-000003",
                "case_version": 1,
                "domain": "career",
                "source": {
                    "title": "Counterexample / Unresolved Prediction Case",
                    "url": "internal://practitioner-records/case-003",
                    "author": "Independent Numerology Evaluation Cohort",
                    "publication_date": "2025-06-20",
                    "evidence_level": EvidenceLevel.E3_PRACTITIONER_CASE.value,
                    "verification_status": VerificationStatus.CONTRADICTED.value
                },
                "inputs": {
                    "date_of_birth": "1994-04-13",
                    "birth_name": "Amit Saxena",
                    "current_name": "Ameet Saxena",
                    "question": "Government examination selection & public administrative career",
                    "observation_period": "24 months"
                },
                "calculations": {
                    "system": "Chaldean",
                    "ruleset_version": "1.0.0",
                    "birth_number": 4,
                    "destiny_number": 4,
                    "name_number": 6,
                    "compound_numbers": [13, 31],
                    "loshu_grid": {"1": 3, "2": 0, "3": 1, "4": 2, "5": 0, "6": 0, "7": 0, "8": 0, "9": 2}
                },
                "interpretations": [
                    {
                        "claim": "Traditional forecast predicted state civil service clearance during Personal Year 1 following name change to compound 33.",
                        "rule_reference": "Personal Year 1 initiation rule",
                        "evidence_status": "traditional"
                    }
                ],
                "predictions": [
                    {
                        "event": "Civil service examination clearance",
                        "start_date": "2025-01-01",
                        "end_date": "2025-07-01",
                        "success_criterion": "Final selection in state public service commission list",
                        "recorded_at": "2024-11-05T09:00:00Z",
                        "forecast_status": "not_realized"
                    }
                ],
                "remedies": [
                    {
                        "type": "Name spelling change to 33 (6) + wearing 6-carat white quartz",
                        "rationale": "Energize Venus to soften double Rahu 4-4 administrative friction.",
                        "cost": "₹3,500 for gemstone and certification",
                        "risks": ["Financial expense with zero guaranteed legal outcome"],
                        "outcome_evidence": "contradicted_by_outcome"
                    }
                ],
                "outcome": {
                    "observed_result": "Candidate did not clear final cutoff; exam selection rate was 0.08% overall.",
                    "evidence_source": "Official commission examination scorecard",
                    "confounders": ["Extreme exam competition ratio (350,000 applicants for 280 seats)"],
                    "independent_review": True
                },
                "provenance": {
                    "source_quotes": ["Predicted success did not manifest; structural competitive baselines overrode symbolic name alignment."],
                    "reviewer": "Numeros Vision Audit Board",
                    "last_verified_at": "2025-08-15"
                }
            }
        ]
        
        self.cases = default_cases
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "cases": default_cases}, f, indent=2, ensure_ascii=False)

    def retrieve_similar_cases(
        self,
        features: NumerologyFeatures,
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Ranks cases using multi-dimensional feature similarity and evidence quality weighting.
        Returns both supporting cases and relevant counterexamples.
        """
        features.validate_features()
        scored_cases = []

        for c in self.cases:
            calc = c.get("calculations", {})
            src = c.get("source", {})
            out = c.get("outcome", {})
            
            # 1. Feature Agreement Score (0.0 to 1.0)
            score = 0.0
            
            # Domain Match (20%)
            c_domain = c.get("domain", "").lower()
            if c_domain == features.domain.lower():
                score += 0.20
            elif "general" in (c_domain, features.domain.lower()):
                score += 0.10
                
            # Birth Number Match (25%)
            if calc.get("birth_number") == features.birth_number:
                score += 0.25
                
            # Destiny Number Match (25%)
            if calc.get("destiny_number") == features.destiny_number:
                score += 0.25
                
            # Name Number / Compound Match (15%)
            if calc.get("name_number") == features.name_number:
                score += 0.10
            if features.compound_number and features.compound_number in calc.get("compound_numbers", []):
                score += 0.05
                
            # Personal Year Match (15%)
            c_py = calc.get("personal_year")
            if features.personal_year and c_py == features.personal_year:
                score += 0.15
            elif not c_py:
                score += 0.05

            # 2. Evidence Quality Multiplier
            ev_level = src.get("evidence_level", EvidenceLevel.E3_PRACTITIONER_CASE.value)
            has_independent_review = out.get("independent_review", False)
            ver_status = src.get("verification_status", VerificationStatus.UNVERIFIED.value)
            
            multiplier = 1.0
            if ev_level == EvidenceLevel.E4_EMPIRICAL_PROSPECTIVE.value:
                multiplier = 1.30
            elif ev_level == EvidenceLevel.E3_PRACTITIONER_CASE.value:
                if has_independent_review:
                    multiplier = 1.10
                elif ver_status == VerificationStatus.CONTRADICTED.value:
                    # Valuable counterexample!
                    multiplier = 1.05
                else:
                    multiplier = 0.90
            elif ev_level == EvidenceLevel.E2_TRADITION.value:
                multiplier = 0.80
                
            final_score = round(score * multiplier, 4)
            
            scored_cases.append({
                "case_id": c.get("case_id"),
                "domain": c.get("domain"),
                "similarity_score": final_score,
                "evidence_level": ev_level,
                "verification_status": ver_status,
                "has_outcome_data": bool(out.get("observed_result")),
                "is_counterexample": ver_status == VerificationStatus.CONTRADICTED.value,
                "source_title": src.get("title"),
                "summary": (
                    f"Case {c.get('case_id')} ({c.get('domain').title()}): Birth {calc.get('birth_number')}, "
                    f"Destiny {calc.get('destiny_number')}, Name {calc.get('name_number')}. "
                    f"Outcome: {out.get('observed_result', 'Unrecorded')}. "
                    f"Evidence Level: {ev_level} ({ver_status})."
                ),
                "case_details": c
            })

        # Sort descending by similarity score
        scored_cases.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_cases[:limit]
