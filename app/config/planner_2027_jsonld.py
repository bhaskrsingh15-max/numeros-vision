"""
NUMEROS VISION — 2027 YEAR AHEAD PLANNER JSON-LD GENERATOR
==========================================================
Generates canonical Product schema.org structured data derived deterministically
from `planner_2027_pricing.json`.
- While waitlist-only (`active=False` or missing price): emits Product WITHOUT `offers`
  or `price` so structured data strictly matches the unpriced "Coming soon, notify me" page.
- When explicitly active with configured prices: emits Product + Offer with server-side
  cutoff support (`now <= offer_ends_at`).
- Strictly zero review or rating markup.
"""

import datetime
import os
from typing import Optional, Dict, Any


def generate_planner_2027_jsonld(
    cfg: Dict[str, Any],
    now: Optional[datetime.datetime] = None
) -> Dict[str, Any]:
    product_ld: Dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": cfg.get("name", "2027 Year Ahead Planner"),
        "description": cfg.get("subtitle", "24-Page Personalized Annual Numerology & Timing Blueprint"),
        "image": "https://numerosvision.com/assets/og-default.png",
        "brand": {
            "@type": "Brand",
            "name": "NUMEROS VISION"
        },
        "url": "https://numerosvision.com/year-2027/"
    }

    env_live = (os.getenv("PLANNER_2027_LIVE") or "").strip().lower() in ("true", "1", "yes")
    is_active = bool(cfg.get("active") is True or env_live) and cfg.get("status") != "waitlist"
    list_paise = cfg.get("list_price_paise")
    offer_paise = cfg.get("offer_price_paise")

    # Waitlist / coming-soon state: strictly zero Offer / price in schema
    if not is_active or list_paise is None:
        return product_ld

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    cutoff_str = cfg.get("offer_ends_at")
    is_offer = False
    if offer_paise is not None and cutoff_str:
        cutoff = datetime.datetime.fromisoformat(cutoff_str)
        is_offer = now <= cutoff

    price = str(int(offer_paise) // 100 if is_offer else int(list_paise) // 100)
    valid_until = cutoff_str[:10] if (is_offer and cutoff_str) else "2027-12-31"

    product_ld["offers"] = {
        "@type": "Offer",
        "price": price,
        "priceCurrency": cfg.get("currency", "INR"),
        "priceValidUntil": valid_until,
        "availability": "https://schema.org/InStock",
        "url": "https://numerosvision.com/year-2027/"
    }
    return product_ld
