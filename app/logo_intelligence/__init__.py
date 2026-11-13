"""
Numeros Vision — Add-Only Logo Intelligence & Brand Studio Package (v1.0)
Reads from existing deterministic numerology and Charm AI correlation engines
without modifying any file in `app/engine/` or `pdf_service/app/engine/`.
"""

from app.logo_intelligence.rulebook_v1 import (
    EvidenceLabel,
    VALID_EVIDENCE_LABELS,
    LogoRulebookV1,
    get_rulebook_v1,
    calculate_contrast_ratio_hex,
    evaluate_contrast_gate,
    classify_hex_colour_family,
    compute_free_scan_verdict,
)

__all__ = [
    "EvidenceLabel",
    "VALID_EVIDENCE_LABELS",
    "LogoRulebookV1",
    "get_rulebook_v1",
    "calculate_contrast_ratio_hex",
    "evaluate_contrast_gate",
    "classify_hex_colour_family",
    "compute_free_scan_verdict",
]
