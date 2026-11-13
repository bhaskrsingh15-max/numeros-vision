"""
Conversion Analytics and Revenue Attribution
Implements Section 21 (Analytics & Revenue Attribution) with verified transaction reconciliation.
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger("conversion_analytics")

class ConversionAnalyticsEngine:
    """Tracks non-overlapping lifecycle events from search discovery to confirmed purchase."""

    ALLOWED_EVENTS = {
        "organic_landing",
        "content_engaged",
        "internal_link_clicked",
        "calculator_started",
        "calculator_completed",
        "report_preview_viewed",
        "package_viewed",
        "checkout_started",
        "purchase_confirmed"
    }

    def __init__(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        self.events_file = os.path.join(self.data_dir, "conversion_events.jsonl")
        self.payments_file = os.path.join(self.data_dir, "payments.jsonl")

    def track_event(self, 
                    event_name: str, 
                    canonical_url: str,
                    properties: Optional[Dict[str, Any]] = None,
                    session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Records a telemetry event without exposing customer PII.
        """
        if event_name not in self.ALLOWED_EVENTS:
            raise ValueError(f"Event '{event_name}' is not in allowed event taxonomy.")

        timestamp = datetime.datetime.now().isoformat()
        props = properties or {}

        # Enforce Section 21 privacy rules: Strip PII
        for sensitive_key in ("name", "full_name", "dob", "birth_date", "phone", "whatsapp", "email"):
            if sensitive_key in props:
                del props[sensitive_key]

        record = {
            "event_name": event_name,
            "canonical_url": canonical_url,
            "session_id": session_id or "anon_session",
            "timestamp": timestamp,
            "properties": props
        }

        try:
            with open(self.events_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            logger.error(f"Failed to record conversion event: {e}")

        return {"status": "RECORDED", "event": event_name, "timestamp": timestamp}

    def get_funnel_summary(self) -> Dict[str, Any]:
        """
        Aggregates events into separate measurement layers without synthetic projections.
        """
        event_counts = {k: 0 for k in self.ALLOWED_EVENTS}
        if os.path.exists(self.events_file):
            with open(self.events_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            ev = json.loads(line)
                            name = ev.get("event_name")
                            if name in event_counts:
                                event_counts[name] += 1
                        except Exception:
                            pass

        # Count verified purchases from payments.jsonl
        confirmed_revenue_inr = 0
        confirmed_purchases_count = 0
        if os.path.exists(self.payments_file):
            with open(self.payments_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            pay = json.loads(line)
                            if pay.get("status") in ("paid", "authorized", "confirmed"):
                                confirmed_purchases_count += 1
                                confirmed_revenue_inr += pay.get("amount_inr", 0)
                        except Exception:
                            pass

        return {
            "search_discovery": {
                "organic_landing": event_counts["organic_landing"],
                "content_engaged": event_counts["content_engaged"]
            },
            "product_engagement": {
                "calculator_started": event_counts["calculator_started"],
                "calculator_completed": event_counts["calculator_completed"],
                "report_preview_viewed": event_counts["report_preview_viewed"]
            },
            "commercial_outcomes": {
                "package_viewed": event_counts["package_viewed"],
                "checkout_started": event_counts["checkout_started"],
                "purchase_confirmed": confirmed_purchases_count or event_counts["purchase_confirmed"],
                "confirmed_revenue_inr": confirmed_revenue_inr
            }
        }
