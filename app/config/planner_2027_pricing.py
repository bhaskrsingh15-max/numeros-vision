"""
Server-side pricing configuration for the 2027 Year Ahead Planner.
Waitlist-only by default (`active = False`, `status = "waitlist"`) until
`{{DISCLAIMER_APPROVED_TEXT}}` is approved and `PLANNER_2027_LIVE=true` is set.
- Client amount is NEVER trusted.
- price_includes_gst = False (Payment receipt wording only).
"""

import os
import json
import datetime
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "planner_2027_pricing.json")
WAITLIST_CAPTION = (
    "When this report opens, it starts at a launch price for its first 7 days. "
    "We\u2019ll email you the day it opens."
)


def load_planner_2027_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def is_planner_2027_live(cfg: Optional[Dict[str, Any]] = None) -> bool:
    env_flag = (os.getenv("PLANNER_2027_LIVE") or "").strip().lower()
    if env_flag in ("true", "1", "yes"):
        return True
    if env_flag in ("false", "0", "no"):
        return False
    loaded = cfg if cfg is not None else load_planner_2027_config()
    return bool(loaded.get("active") is True and loaded.get("status") != "waitlist")


def get_planner_2027_price(
    now: Optional[datetime.datetime] = None,
    cfg_override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Returns current pricing details for 2027 Year Ahead Planner.
    When waitlist-only (`active=False` / `PLANNER_2027_LIVE != 'true'`), returns
    strictly null prices and `status="waitlist"`.
    """
    cfg = dict(cfg_override) if cfg_override is not None else load_planner_2027_config()
    live = is_planner_2027_live(cfg)
    list_paise = cfg.get("list_price_paise")
    offer_paise = cfg.get("offer_price_paise")
    offer_ends_str = cfg.get("offer_ends_at")

    if not live or list_paise is None:
        return {
            "list": None,
            "offer": None,
            "amount_paise": None,
            "currency": cfg.get("currency", "INR"),
            "offer_ends_at": None,
            "active": False,
            "status": "waitlist",
            "waitlist_only": True,
            "waitlist_label": cfg.get("waitlist_label", "Coming soon, notify me"),
            "waitlist_caption": cfg.get("waitlist_caption", WAITLIST_CAPTION),
            "is_offer_active": False,
            "price_includes_gst": cfg.get("price_includes_gst", False),
            "receipt_type": cfg.get("receipt_type", "Payment receipt"),
        }

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    is_offer_active = False
    if offer_paise is not None and offer_ends_str:
        offer_ends_dt = datetime.datetime.fromisoformat(offer_ends_str)
        is_offer_active = now < offer_ends_dt

    charged_amount = int(offer_paise) if is_offer_active else int(list_paise)
    return {
        "list": int(list_paise),
        "offer": int(offer_paise) if offer_paise is not None else None,
        "amount_paise": charged_amount,
        "currency": cfg.get("currency", "INR"),
        "offer_ends_at": offer_ends_str,
        "active": True,
        "status": "active",
        "waitlist_only": False,
        "is_offer_active": is_offer_active,
        "price_includes_gst": cfg.get("price_includes_gst", False),
        "receipt_type": cfg.get("receipt_type", "Payment receipt"),
    }
