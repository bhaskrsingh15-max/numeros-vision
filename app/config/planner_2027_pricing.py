"""
Server-side pricing configuration for the 2027 Year Ahead Planner.
Pricing rules:
- list_price_paise: 199900 (INR 1,999)
- offer_price_paise: 149900 (INR 1,499)
- offer_ends_at: 2027-01-31T23:59:00+05:30
- Server determines charge amount based on now < offer_ends_at.
- Client amount is NEVER trusted.
- price_includes_gst = False (Payment receipt wording only).
"""

import os
import json
import datetime
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "planner_2027_pricing.json")


def load_planner_2027_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_planner_2027_price(now: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """
    Returns current pricing details:
    {
        "list": 199900,
        "offer": 149900,
        "amount_paise": 149900 (or 199900 if expired),
        "currency": "INR",
        "offer_ends_at": "2027-01-31T23:59:00+05:30",
        "active": True,
        "is_offer_active": True/False,
        "price_includes_gst": False,
        "receipt_type": "Payment receipt"
    }
    """
    cfg = load_planner_2027_config()
    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    # Parse offer_ends_at with timezone
    offer_ends_dt = datetime.datetime.fromisoformat(cfg["offer_ends_at"])
    is_offer_active = now < offer_ends_dt

    charged_amount = cfg["offer_price_paise"] if is_offer_active else cfg["list_price_paise"]

    return {
        "list": cfg["list_price_paise"],
        "offer": cfg["offer_price_paise"],
        "amount_paise": charged_amount,
        "currency": cfg["currency"],
        "offer_ends_at": cfg["offer_ends_at"],
        "active": True,
        "is_offer_active": is_offer_active,
        "price_includes_gst": cfg.get("price_includes_gst", False),
        "receipt_type": cfg.get("receipt_type", "Payment receipt"),
    }
