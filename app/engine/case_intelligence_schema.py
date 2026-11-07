# -*- coding: utf-8 -*-
"""
CASE INTELLIGENCE SCHEMA & EVIDENCE HIERARCHY
Numeros Vision — Master Knowledge Engine
Defines the strict 4-tier evidence model (E1-E4), feature validation,
and auditable case records for case matching and prediction tracking.
In strict compliance with Master AGENTS.md.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


class EvidenceLevel(str, Enum):
    """
    Four-Tier Evidence Classification for Numeros Vision:
    E1: Reproducible arithmetic and documented structural rules.
    E2: Published traditional canon (Chaldean, Pythagorean, Vedic, Lo Shu).
    E3: Practitioner-reported cases (anecdotal, observational, unverified).
    E4: Independently evaluated prospective results on unseen cohorts.
    DISPUTED: Claims that fail testing, show high contradiction, or lack provenance.
    """
    E1_ARITHMETIC = "E1"
    E2_TRADITION = "E2"
    E3_PRACTITIONER_CASE = "E3"
    E4_EMPIRICAL_PROSPECTIVE = "E4"
    DISPUTED = "DISPUTED"


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONTRADICTED = "contradicted"


@dataclass(frozen=True)
class NumerologyFeatures:
    """
    Deterministic feature vector extracted from client birth and name data.
    Ensures multi-dimensional comparison rather than naive single-number lookups.
    """
    birth_number: int
    destiny_number: int
    name_number: int
    compound_number: Optional[int]
    personal_year: Optional[int]
    domain: str

    def feature_key(self) -> Tuple[int, int, int, Optional[int], Optional[int], str]:
        return (
            self.birth_number,
            self.destiny_number,
            self.name_number,
            self.compound_number,
            self.personal_year,
            self.domain.lower(),
        )

    def validate_features(self) -> None:
        """Enforces boundary rules across all feature dimensions."""
        for val, name in [
            (self.birth_number, "Birth number"),
            (self.destiny_number, "Destiny number"),
            (self.name_number, "Name number"),
        ]:
            if not 1 <= val <= 9:
                raise ValueError(f"{name} must be a single digit between 1 and 9 (received {val})")
        
        if self.compound_number is not None and self.compound_number < 1:
            raise ValueError(f"Compound number must be positive (received {self.compound_number})")
            
        if self.personal_year is not None and not 1 <= self.personal_year <= 9:
            raise ValueError(f"Personal year must be between 1 and 9 (received {self.personal_year})")
            
        if not self.domain or not self.domain.strip():
            raise ValueError("Domain is required (e.g., 'career', 'marriage', 'wealth', 'health')")


@dataclass
class CaseRecord:
    """
    Auditable Case Intelligence Record.
    Null values are strictly preserved where the historical source lacks data.
    The ingestion engine must never manufacture missing values.
    """
    case_id: str
    case_version: int = 1
    domain: str = "general"
    source: Dict[str, Any] = field(default_factory=lambda: {
        "title": None,
        "url": None,
        "author": None,
        "publication_date": None,
        "evidence_level": EvidenceLevel.E3_PRACTITIONER_CASE.value,
        "verification_status": VerificationStatus.UNVERIFIED.value
    })
    inputs: Dict[str, Any] = field(default_factory=lambda: {
        "date_of_birth": None,
        "birth_name": None,
        "current_name": None,
        "question": None,
        "observation_period": None
    })
    calculations: Dict[str, Any] = field(default_factory=lambda: {
        "system": "Chaldean",
        "ruleset_version": "1.0.0",
        "birth_number": None,
        "destiny_number": None,
        "name_number": None,
        "compound_numbers": [],
        "loshu_grid": None
    })
    interpretations: List[Dict[str, Any]] = field(default_factory=list)
    predictions: List[Dict[str, Any]] = field(default_factory=list)
    remedies: List[Dict[str, Any]] = field(default_factory=list)
    outcome: Dict[str, Any] = field(default_factory=lambda: {
        "observed_result": None,
        "evidence_source": None,
        "confounders": [],
        "independent_review": False
    })
    provenance: Dict[str, Any] = field(default_factory=lambda: {
        "source_quotes": [],
        "reviewer": None,
        "last_verified_at": None
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_version": self.case_version,
            "domain": self.domain,
            "source": self.source,
            "inputs": self.inputs,
            "calculations": self.calculations,
            "interpretations": self.interpretations,
            "predictions": self.predictions,
            "remedies": self.remedies,
            "outcome": self.outcome,
            "provenance": self.provenance
        }
