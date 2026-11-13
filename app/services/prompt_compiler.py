"""
Numeros Vision — Customer-Specific Prompt Compiler
Implements Section 17.5 of the Master Build Specification.
Deterministically compiles customer-specific prompts from validated DesignSpecifications,
applying prompt-injection sanitization, exact wordmark quotation, and versioned hashing.
"""

from typing import Dict, Any, Tuple
import hashlib
import re
from app.services.design_specification import DesignSpecification, DesignSpecificationValidator


class PromptCompiler:
    """
    Deterministic compiler for Google Nano Banana / Gemini image generation prompts.
    Does NOT use an LLM to invent rules or missing colors.
    """

    PROMPT_TEMPLATE_VERSION = "1.0.0"

    INJECTION_PATTERN = re.compile(
        r"(ignore\s+(all\s+)?previous\s+instructions|system\s+prompt|admin\s+override|<script|;\s*drop\s+table)",
        re.IGNORECASE
    )

    @classmethod
    def sanitize_field(cls, text: str) -> str:
        """Strips control tokens, newlines, and prompt injection patterns from user strings."""
        if not text:
            return ""
        # Remove dangerous prompt injection keywords
        cleaned = cls.INJECTION_PATTERN.sub("[redacted]", text)
        # Normalize whitespace (replace multiple newlines and tabs)
        cleaned = " ".join(cleaned.split())
        return cleaned.strip()

    @classmethod
    def compile(cls, spec: DesignSpecification, require_approval: bool = True) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Compiles a customer-specific prompt matching Section 17.5.
        Returns:
            (success: bool, compiled_prompt: str, metadata: Dict[str, Any])
        """
        is_valid, errors = DesignSpecificationValidator.validate(spec, require_customer_approval=require_approval)
        if not is_valid:
            return False, "", {
                "error": "Validation failed for DesignSpecification",
                "validation_errors": errors,
            }

        # 1. Sanitize business & audience fields
        wordmark = cls.sanitize_field(spec.business.exact_wordmark)
        activity = cls.sanitize_field(spec.business.activity)
        audience = cls.sanitize_field(", ".join(spec.business.audience) if spec.business.audience else "general public")
        market = cls.sanitize_field(", ".join(spec.business.market) if spec.business.market else "global")
        positioning = cls.sanitize_field(", ".join(spec.business.positioning) if spec.business.positioning else "premium quality")
        attributes = cls.sanitize_field(", ".join(spec.visual_direction.brand_attributes) if spec.visual_direction.brand_attributes else "modern, distinctive")

        # 2. Extract Palette roles
        primary_color = "Gold #C9A227"
        secondary_color = "Pearl White #FFFDF7"
        accent_color = "Emerald #16835B"
        background_color = "Transparent or Clean Pearl White #FFFDF7"

        for item in spec.visual_direction.palette:
            formatted = f"{cls.sanitize_field(item.name)} {item.hex.upper()}"
            if item.role == "primary":
                primary_color = formatted
            elif item.role == "secondary":
                secondary_color = formatted
            elif item.role == "accent":
                accent_color = formatted
            elif item.role == "background":
                background_color = formatted

        # 3. Geometry & Symbol
        concept = cls.sanitize_field(spec.visual_direction.symbol_concept or "minimalist, balanced geometric mark")
        composition = cls.sanitize_field(spec.visual_direction.composition or "balanced symbol and wordmark lockup")
        geometry = cls.sanitize_field(", ".join(spec.visual_direction.geometry_and_motion) or "clean forward motion and harmonious symmetry")

        # 4. Required & Avoid
        must_include = cls.sanitize_field(", ".join(spec.visual_direction.must_include) or "clean silhouette, high scalability")
        must_avoid = cls.sanitize_field(
            ", ".join(spec.visual_direction.must_avoid)
            or "unrequested symbols, extra text, watermark-like decorations, 3D mockups, gradients, visual clutter"
        )

        # 5. Build prompt strictly following Section 17.5 template
        compiled_prompt = (
            f'Create an original professional logo concept for the customer-approved brand:\n'
            f'"{wordmark}"\n\n'
            f'Business and audience:\n'
            f'{activity}, serving {audience} in the {market} market, positioned as {positioning}.\n\n'
            f'Brand positioning and attributes:\n'
            f'{attributes}.\n\n'
            f'Design concept:\n'
            f'{concept}, emphasizing {geometry}.\n\n'
            f'Palette:\n'
            f'- Primary: {primary_color}\n'
            f'- Secondary: {secondary_color}\n'
            f'- Accent: {accent_color}\n'
            f'- Background: {background_color}\n\n'
            f'Typography:\n'
            f'Clean, highly legible typography. Render only the exact wordmark "{wordmark}".\n'
            f'Do not add, remove, misspell, translate, abbreviate or repeat any letters.\n'
            f'If exact text cannot be rendered reliably, prioritize a clean symbol-only concept\n'
            f'and flag the wordmark for deterministic typesetting after generation.\n\n'
            f'Composition:\n'
            f'{composition}, with generous clear space and optical balance.\n\n'
            f'Required:\n'
            f'{must_include}.\n\n'
            f'Must avoid:\n'
            f'{must_avoid}.\n\n'
            f'Reference image handling:\n'
            f'Maintain core geometric proportions if customer reference supplied; otherwise create fresh vector geometry.\n\n'
            f'Output:\n'
            f'A clean, distinctive logo concept suitable for review at small and large sizes.\n'
            f'Keep shapes simple enough to reproduce in monochrome and vector form.\n'
            f'Do not claim or depict any numerology, astrology or business result as proven fact.\n'
            f'Do not imitate a third-party logo or use unlicensed brand assets.'
        )

        prompt_hash = hashlib.sha256(compiled_prompt.encode("utf-8")).hexdigest()

        metadata = {
            "prompt_template_version": cls.PROMPT_TEMPLATE_VERSION,
            "prompt_hash": prompt_hash,
            "exact_wordmark": wordmark,
            "project_id": spec.project_id,
            "validation_checklist": [
                "exact_wordmark_ocr_check",
                "palette_hex_sampling_check",
                "wcag_contrast_ratio_check",
                "dimension_and_mime_check",
                "small_size_legibility_check",
            ],
        }

        return True, compiled_prompt, metadata
