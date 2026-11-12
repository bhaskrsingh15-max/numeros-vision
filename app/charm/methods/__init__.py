"""
app/charm/methods/__init__.py
=============================
Independent Tradition Adapters for Charm AI:
1. KP Astrology (kp_adapter)
2. Vedic Parashari Jyotish (vedic_adapter)
3. Bhrigu Nandi Nadi (bnn_adapter)
4. Western Pythagorean Numerology (pythagorean_adapter)
5. Vedic Sankhya Shastra (vedic_numerology_adapter)
6. Lal Kitab (lal_kitab_adapter - Safely Gated / Disabled)
"""

from app.charm.methods.kp_adapter import kp_adapter, KPMethodAdapter, MethodEvaluation
from app.charm.methods.vedic_adapter import vedic_adapter, VedicMethodAdapter
from app.charm.methods.bnn_adapter import bnn_adapter, BNNMethodAdapter
from app.charm.methods.pythagorean_adapter import pythagorean_adapter, PythagoreanMethodAdapter
from app.charm.methods.vedic_numerology_adapter import vedic_numerology_adapter, VedicNumerologyMethodAdapter
from app.charm.methods.lal_kitab_adapter import lal_kitab_adapter, LalKitabGatedAdapter

__all__ = [
    "kp_adapter",
    "vedic_adapter",
    "bnn_adapter",
    "pythagorean_adapter",
    "vedic_numerology_adapter",
    "lal_kitab_adapter",
    "KPMethodAdapter",
    "VedicMethodAdapter",
    "BNNMethodAdapter",
    "PythagoreanMethodAdapter",
    "VedicNumerologyMethodAdapter",
    "LalKitabGatedAdapter",
    "MethodEvaluation"
]
