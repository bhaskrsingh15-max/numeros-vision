"""
NUMEROS VISION — 2027 YEAR AHEAD PLANNER JSON-LD GENERATOR
==========================================================
Generates canonical Product + Offer schema.org structured data
derived deterministically from planner_2027_pricing.json.
Supports arbitrary timestamp evaluation for post-offer cutoff testing.
"""

import datetime
from typing import Optional, Dict, Any


def generate_planner_2027_jsonld(
    cfg: Dict[str, Any],
    now: Optional[datetime.datetime] = None
) -> Dict[str, Any]:
    """
    Builds the Product + Offer JSON-LD structured data.
    - If `now` is before `offer_ends_at`: price is offer_price_paise // 100, validUntil is offer cutoff.
    - If `now` is after `offer_ends_at`: price is list_price_paise // 100, validUntil is 2027-12-31.
    - Strictly zero review or rating markup.
    """
    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    cutoff_str = cfg.get("offer_ends_at", "2027-01-31T23:59:00+05:30")
    cutoff = datetime.datetime.fromisoformat(cutoff_str)

    is_offer = now <= cutoff
    price = str(cfg["offer_price_paise"] // 100 if is_offer else cfg["list_price_paise"] // 100)
    valid_until = cutoff_str[:10] if is_offer else "2027-12-31"

    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": cfg.get("name", "2027 Year Ahead Planner"),
        "description": cfg.get("subtitle", "24-Page Personalized Annual Astrological & Vibrational Blueprint"),
        "image": "https://numerosvision.com/logos/nv-logo-mark.svg",
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": cfg.get("currency", "INR"),
            "priceValidUntil": valid_until,
            "availability": "https://schema.org/InStock",
            "url": "https://numerosvision.com/year_2027.html"
        }
    }
