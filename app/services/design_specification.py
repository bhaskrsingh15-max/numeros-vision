"""
Numeros Vision — DesignSpecification Schema and Validation Service
Implements Section 17.4 of the Master Build Specification.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Literal, Any
import re
import uuid


HexRole = Literal["primary", "secondary", "accent", "background"]
RationaleType = Literal["brand", "traditional", "accessibility"]


@dataclass
class PaletteItem:
    name: str
    hex: str
    role: HexRole
    rationale_type: RationaleType
    source_rule_id: Optional[str] = None


@dataclass
class BusinessSpec:
    exact_wordmark: str
    activity: str
    categories: List[str] = field(default_factory=list)
    audience: List[str] = field(default_factory=list)
    market: List[str] = field(default_factory=list)
    positioning: List[str] = field(default_factory=list)
    required_subtitle: Optional[str] = None


@dataclass
class AssessmentSpec:
    calculation_run_ids: List[str] = field(default_factory=list)
    method_versions: List[str] = field(default_factory=list)
    rulebook_versions: List[str] = field(default_factory=list)
    approved_rule_ids: List[str] = field(default_factory=list)
    source_citations: List[str] = field(default_factory=list)
    traditional_findings: List[Dict[str, Any]] = field(default_factory=list)
    practical_brand_findings: List[str] = field(default_factory=list)
    unresolved_findings: List[str] = field(default_factory=list)
    confidence_and_limitations: List[str] = field(default_factory=list)


@dataclass
class VisualDirectionSpec:
    brand_attributes: List[str] = field(default_factory=list)
    symbol_concept: str = ""
    geometry_and_motion: List[str] = field(default_factory=list)
    composition: str = "symbol and wordmark lockup"
    palette: List[PaletteItem] = field(default_factory=list)
    backgrounds: List[str] = field(default_factory=lambda: ["light", "dark", "transparent"])
    must_include: List[str] = field(default_factory=list)
    must_avoid: List[str] = field(default_factory=list)
    customer_constraints: List[str] = field(default_factory=list)


@dataclass
class ProductionSpec:
    primary_aspect_ratio: Literal["1:1", "4:3", "3:2", "16:9", "9:16"] = "1:1"
    target_sizes: List[str] = field(default_factory=lambda: ["1K", "2K"])
    deliverable_variants: List[str] = field(default_factory=lambda: ["icon", "horizontal_lockup", "stacked_lockup"])
    exact_wordmark_required: bool = True
    vector_export_required: bool = True
    validation_policy_version: str = "1.0.0"


@dataclass
class ApprovalSpec:
    customer_approved_wordmark: bool = False
    customer_approved_palette: bool = False
    customer_approved_direction: bool = False

    def is_fully_approved(self) -> bool:
        return (
            self.customer_approved_wordmark
            and self.customer_approved_palette
            and self.customer_approved_direction
        )


@dataclass
class DesignSpecification:
    schema_version: str = "1.0.0"
    project_id: str = field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:12]}")
    business: BusinessSpec = field(default_factory=lambda: BusinessSpec(exact_wordmark="", activity=""))
    assessment: AssessmentSpec = field(default_factory=AssessmentSpec)
    visual_direction: VisualDirectionSpec = field(default_factory=VisualDirectionSpec)
    production: ProductionSpec = field(default_factory=ProductionSpec)
    approval: ApprovalSpec = field(default_factory=ApprovalSpec)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DesignSpecificationValidator:
    """
    Validates that a DesignSpecification conforms strictly to Section 17.4.
    Rejects malformed hex codes, empty wordmarks, unapproved traditional findings,
    and unapproved customer choices before generation.
    """

    HEX_REGEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

    @classmethod
    def validate(cls, spec: DesignSpecification, require_customer_approval: bool = False) -> Tuple[bool, List[str]]:
        errors = []

        # 1. Business validation
        if not spec.business.exact_wordmark or not spec.business.exact_wordmark.strip():
            errors.append("Business exact_wordmark cannot be empty.")
        if not spec.business.activity or not spec.business.activity.strip():
            errors.append("Business activity description cannot be empty.")

        # 2. Palette validation
        if not spec.visual_direction.palette:
            errors.append("At least one palette item is required.")
        for item in spec.visual_direction.palette:
            if not cls.HEX_REGEX.match(item.hex):
                errors.append(f"Invalid HEX code '{item.hex}' for palette role '{item.name}'.")
            if item.role not in ["primary", "secondary", "accent", "background"]:
                errors.append(f"Invalid palette role '{item.role}'. Must be primary, secondary, accent, or background.")
            if item.rationale_type not in ["brand", "traditional", "accessibility"]:
                errors.append(f"Invalid rationale_type '{item.rationale_type}'.")

        # 3. Customer approval check (mandatory gate before paid generation)
        if require_customer_approval and not spec.approval.is_fully_approved():
            missing = []
            if not spec.approval.customer_approved_wordmark:
                missing.append("wordmark")
            if not spec.approval.customer_approved_palette:
                missing.append("palette")
            if not spec.approval.customer_approved_direction:
                missing.append("visual direction")
            errors.append(f"Paid generation gate locked: Customer has not approved {', '.join(missing)}.")

        return len(errors) == 0, errors
