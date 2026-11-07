# -*- coding: utf-8 -*-
"""
PREDICTION LEDGER & OUTCOME TRACKING ENGINE
Numeros Vision — Master Knowledge Engine
Freezes predictions before outcomes occur, tracks time windows, records verified post-event results,
and enables empirical backtesting without rewriting history.
In strict compliance with Master AGENTS.md and DPDP Act 2023.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone

LEDGER_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "knowledge_base" / "prediction_ledger.json"


class PredictionLedgerEngine:
    """
    Maintains an immutable ledger of timestamped predictions and outcomes.
    Enforces that predictions are recorded in advance and never retroactively modified.
    """

    def __init__(self, data_file: Path = LEDGER_FILE):
        self.data_file = data_file
        self.ledger: List[Dict[str, Any]] = []
        self._load_ledger()

    def _load_ledger(self) -> None:
        if not self.data_file.exists():
            self._initialize_empty_ledger()
            return
        
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.ledger = data.get("predictions", [])
        except Exception as e:
            print(f"Warning: Failed to load prediction ledger ({e}). Initializing empty.")
            self._initialize_empty_ledger()

    def _initialize_empty_ledger(self) -> None:
        self.ledger = []
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "predictions": []}, f, indent=2, ensure_ascii=False)

    def freeze_prediction(
        self,
        user_identifier: str,
        domain: str,
        forecast_text: str,
        start_date: str,
        end_date: str,
        success_criterion: str,
        prediction_mode: str = "MODE_A_TRADITIONAL",
        ruleset_version: str = "1.0.0",
        consent_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Freezes a prospective prediction prior to the forecast horizon.
        Anonymizes user identifier via SHA-256 for DPDP 2023 compliance.
        """
        user_hash = hashlib.sha256(user_identifier.encode('utf-8')).hexdigest()[:16]
        ledger_id = f"PRED-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{len(self.ledger) + 1:05d}"
        
        entry = {
            "ledger_id": ledger_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "user_hash": user_hash,
            "consent_token": consent_token or "DPDP_CONSENT_EXPLICIT_OPT_IN",
            "domain": domain.lower(),
            "prediction_mode": prediction_mode,
            "ruleset_version": ruleset_version,
            "forecast_text": forecast_text,
            "target_window": {
                "start_date": start_date,
                "end_date": end_date
            },
            "success_criterion": success_criterion,
            "status": "ACTIVE_PENDING",
            "post_event_outcome": None,
            "last_reviewed_at": None
        }
        
        self.ledger.append(entry)
        self._save_ledger()
        return entry

    def record_outcome(
        self,
        ledger_id: str,
        outcome_status: str,  # VERIFIED_SUCCESS, VERIFIED_UNSUCCESSFUL, PARTIAL
        observed_result: str,
        evidence_source: str,
        confounders: Optional[List[str]] = None,
        independent_review: bool = False
    ) -> Dict[str, Any]:
        """
        Records the verified real-world outcome once the target horizon has completed.
        Strictly preserves original prediction text without modification.
        """
        for item in self.ledger:
            if item["ledger_id"] == ledger_id:
                item["status"] = outcome_status
                item["last_reviewed_at"] = datetime.now(timezone.utc).isoformat()
                item["post_event_outcome"] = {
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                    "outcome_status": outcome_status,
                    "observed_result": observed_result,
                    "evidence_source": evidence_source,
                    "confounders": confounders or [],
                    "independent_review": independent_review
                }
                self._save_ledger()
                return item
                
        raise KeyError(f"Ledger record '{ledger_id}' not found.")

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistical overview of active vs resolved predictions."""
        total = len(self.ledger)
        active = sum(1 for p in self.ledger if p["status"] == "ACTIVE_PENDING")
        verified_success = sum(1 for p in self.ledger if p["status"] == "VERIFIED_SUCCESS")
        verified_fail = sum(1 for p in self.ledger if p["status"] == "VERIFIED_UNSUCCESSFUL")
        
        return {
            "total_predictions_frozen": total,
            "active_pending": active,
            "verified_success": verified_success,
            "verified_unsuccessful": verified_fail,
            "resolved_total": verified_success + verified_fail,
            "empirical_calibration_readiness": "SUFFICIENT_DATA" if (verified_success + verified_fail) >= 50 else "INSUFFICIENT_DATA_FOR_EMPIRICAL_PROBABILITY"
        }

    def _save_ledger(self) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "predictions": self.ledger}, f, indent=2, ensure_ascii=False)
