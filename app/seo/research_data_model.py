"""
Numeros Vision — Research Data Model & Evidence Provenance Layer
Implements Section 4 (Search Data Model) & Section 11 (Claim Ledger Schema)
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Dict, Any
import datetime
import uuid


class EvidenceStatus(str, Enum):
    OBSERVED = "OBSERVED"
    PROVIDER_REPORTED = "PROVIDER_REPORTED"
    FIRST_PARTY_VERIFIED = "FIRST_PARTY_VERIFIED"
    MODEL_SUGGESTED = "MODEL_SUGGESTED"
    USER_PROVIDED_UNVERIFIED = "USER_PROVIDED_UNVERIFIED"
    CONFLICTING = "CONFLICTING"
    STALE = "STALE"
    REJECTED = "REJECTED"


class SearchIntent(str, Enum):
    INFORMATIONAL = "INFORMATIONAL"
    TOOL_SEEKING = "TOOL_SEEKING"
    COMMERCIAL_INVESTIGATION = "COMMERCIAL_INVESTIGATION"
    TRANSACTIONAL = "TRANSACTIONAL"
    NAVIGATIONAL = "NAVIGATIONAL"
    LOCAL_SERVICE = "LOCAL_SERVICE"
    MIXED = "MIXED"
    UNCLASSIFIED = "UNCLASSIFIED"


class ClaimType(str, Enum):
    OFFICIAL_DOCUMENTATION = "OFFICIAL_DOCUMENTATION"
    FIRST_PARTY_PRODUCT_FACT = "FIRST_PARTY_PRODUCT_FACT"
    HISTORICAL_FACT = "HISTORICAL_FACT"
    NUMEROLOGY_TRADITION = "NUMEROLOGY_TRADITION"
    MARKET_STATISTIC = "MARKET_STATISTIC"
    PRICING_OR_OFFER = "PRICING_OR_OFFER"
    LEGAL_OR_PRIVACY = "LEGAL_OR_PRIVACY"


class ClaimStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNVERIFIED = "UNVERIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass
class ResearchRecord:
    research_record_id: str = field(default_factory=lambda: f"REC-{uuid.uuid4().hex[:8].upper()}")
    provider: str = "AnswerThePublic"
    provider_record_id: Optional[str] = None
    source_type: str = "CSV_IMPORT"
    seed_keyword: str = "numerology"
    keyword_text: str = ""
    normalized_keyword: str = ""
    platform: str = "Google"
    country: str = "in"
    language: str = "en"
    search_intent: SearchIntent = SearchIntent.INFORMATIONAL
    topic_cluster: str = "Core Numerology"
    search_volume: Optional[int] = None
    volume_period: str = "Monthly Average"
    volume_source: str = "AnswerThePublic"
    volume_definition: str = "Estimated 30-day Google Search volume (India, en)"
    cpc: Optional[float] = None
    cpc_currency: str = "USD"
    evidence_status: EvidenceStatus = EvidenceStatus.PROVIDER_REPORTED
    observed_at: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d"))
    target_url: Optional[str] = None
    confidence_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["search_intent"] = self.search_intent.value
        d["evidence_status"] = self.evidence_status.value
        return d


@dataclass
class ClaimLedgerEntry:
    claim_id: str = field(default_factory=lambda: f"CLM-{uuid.uuid4().hex[:8].upper()}")
    content_id: str = ""
    claim_text: str = ""
    claim_type: ClaimType = ClaimType.NUMEROLOGY_TRADITION
    source_title: str = ""
    source_url: str = ""
    source_publisher: str = "Numeros Vision Source Registry"
    source_date: str = "1926"
    supporting_excerpt: str = ""
    verification_status: ClaimStatus = ClaimStatus.SUPPORTED
    reviewer: str = "Automated Claim Validator"
    reviewed_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["claim_type"] = self.claim_type.value
        d["verification_status"] = self.verification_status.value
        return d


@dataclass
class ContentBrief:
    brief_id: str = field(default_factory=lambda: f"BRF-{uuid.uuid4().hex[:8].upper()}")
    working_title: str = ""
    target_url: str = ""
    page_type: str = "Educational Guide"
    primary_keyword: str = ""
    secondary_keywords: List[str] = field(default_factory=list)
    intent: SearchIntent = SearchIntent.INFORMATIONAL
    reader_outcome: str = ""
    proposed_outline: List[str] = field(default_factory=list)
    required_claims: List[ClaimLedgerEntry] = field(default_factory=list)
    required_sources: List[str] = field(default_factory=list)
    methodology_requirements: str = "Deterministic 6-tradition arithmetic"
    product_relevance: str = ""
    offer_id: Optional[str] = None
    cta_allowed: bool = False
    schema_candidates: List[str] = field(default_factory=lambda: ["Article", "FAQPage", "BreadcrumbList"])
    image_requirements: Dict[str, Any] = field(default_factory=lambda: {
        "needs_diagram": True,
        "purpose": "EXPLANATORY_DIAGRAM",
        "aspect_ratio": "16:9",
        "suggested_alt": "",
        "suggested_caption": ""
    })
    brief_status: str = "APPROVED"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["intent"] = self.intent.value
        d["required_claims"] = [c.to_dict() if hasattr(c, "to_dict") else c for c in self.required_claims]
        return d
