"""Brand report generation utilities for the Logo Studio page.

This module provides a deterministic function that assembles the core
numerology and archetype analysis required for the free/paid report.
It purposefully avoids any external network calls – all calculations are
performed by the existing deterministic engines in ``app.engine``.

The public API is :func:`generate_brand_report` which returns a plain
Python ``dict`` that can be JSON‑serialised and rendered in a Jinja
template.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

from app.engine.business_taxonomy import BusinessTaxonomyEngine
from app.engine.archetype_engine import ContextualArchetypeEngine
from app.engine.core_matrix_engine import (
    calculate_chaldean_name,
    generate_core_matrix_profile,
)

logger = logging.getLogger(__name__)

# Re‑use singleton engines – they are inexpensive and stateless.
_taxonomy_engine = BusinessTaxonomyEngine()
_archetype_engine = ContextualArchetypeEngine()


def _calc_founder_profile(business_name: str, dob: str) -> Optional[Dict[str, int]]:
    """Calculate a Core‑Matrix profile for the founder if a valid DOB is given.

    ``dob`` must be a ``YYYY‑MM‑DD`` string.  On any parsing error ``None`` is
    returned – the caller should treat the founder metrics as unavailable.
    """
    try:
        year, month, day = map(int, dob.split("-"))
    except Exception as exc:  # pragma: no cover – defensive
        logger.debug("Invalid DOB %s: %s", dob, exc)
        return None

    # The deterministic engine expects day, month, year and a gender.  For the
    # purpose of the free report we default to "male" – the gender does not
    # affect the numeric core matrix values used downstream.
    profile = generate_core_matrix_profile(
        name=business_name,
        day=day,
        month=month,
        year=year,
        gender="male",
    )
    return profile


def generate_brand_report(
    business_name: str,
    business_activity: str,
    founder_dob: Optional[str] = None,
) -> Dict:
    """Create a deterministic brand‑analysis payload.

    The returned dictionary contains:

    * ``business_name`` – echo of the input.
    * ``taxonomy`` – primary category determined by ``BusinessTaxonomyEngine``.
    * ``chaldean`` – ``compound`` (numeric) and ``root`` (single digit).
    * ``founder_profile`` – optional Core‑Matrix profile.
    * ``archetype`` – result of ``ContextualArchetypeEngine.evaluate``.
    * ``aligned`` – ``True`` when the archetype evaluation returns a
      ``status`` of ``aligned``.
    """
    # 1️⃣ Business taxonomy
    taxonomy_res = _taxonomy_engine.classify(business_name, business_activity)
    primary_category = taxonomy_res.get("primary_category", "unknown")

    # 2️⃣ Chaldean numerology for the business name
    chaldean_res = calculate_chaldean_name(business_name)
    # ``calculate_chaldean_name`` returns a dict with ``compound`` and ``root``
    # keys – we pass them through directly.

    # 3️⃣ Optional founder profile
    founder_profile = None
    if founder_dob:
        founder_profile = _calc_founder_profile(business_name, founder_dob)

    # 4️⃣ Contextual archetype evaluation (deterministic)
    archetype_res = _archetype_engine.evaluate(
        business_name=business_name,
        business_activity=business_activity,
        category=primary_category,
        chaldean=chaldean_res,
        founder_profile=founder_profile,
    )
    aligned = archetype_res.get("status", "unaligned") == "aligned"

    report = {
        "business_name": business_name,
        "business_activity": business_activity,
        "taxonomy": {
            "primary_category": primary_category,
            "details": taxonomy_res,
        },
        "chaldean": {
            "compound": chaldean_res.get("compound"),
            "root": chaldean_res.get("root"),
        },
        "founder_profile": founder_profile,
        "archetype": archetype_res,
        "aligned": aligned,
    }
    return report
