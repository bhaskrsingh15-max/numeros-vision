"""
app/charm/outcomes/outcome_service.py
======================================
Prediction Snapshot & User Outcome Tracking Service for Charm AI.
Complies with Section 10 and 13 of Master Specification v2.0.
"""

from datetime import datetime
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

OUTCOMES_FILE = Path(__file__).resolve().parent.parent.parent.parent / "data" / "charm_ai_outcomes_ledger.json"

class PredictionSnapshot(BaseModel):
    prediction_id: str
    user_id: str
    created_at: str
    event_definition_id: str
    event_family: str
    driver: int
    conductor: int
    personal_year: int
    verification_status: str
    event_assessment: str
    primary_windows: List[Dict[str, Any]]
    method_evaluations: List[Dict[str, Any]]
    citations: List[Dict[str, Any]]
    policy_version: str

class OutcomeRecord(BaseModel):
    outcome_id: str
    prediction_id: str
    user_id: str
    recorded_at: str
    outcome_status: str = Field(
        ...,
        description="PENDING, OCCURRED_WITHIN_WINDOW, OCCURRED_LATER, DID_NOT_OCCUR_WITHIN_WINDOW, UNSURE, DECLINED, LOST_TO_FOLLOW_UP, NOT_SCORABLE"
    )
    user_comment: Optional[str] = None
    is_verified_cohort: bool = False

class OutcomeService:
    def __init__(self, ledger_file: Path = OUTCOMES_FILE):
        self.ledger_file = ledger_file
        self._snapshots: Dict[str, PredictionSnapshot] = {}
        self._outcomes: Dict[str, OutcomeRecord] = {}
        self._load_ledger()

    def _load_ledger(self):
        if self.ledger_file.exists():
            try:
                with open(self.ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for s in data.get("snapshots", []):
                        self._snapshots[s["prediction_id"]] = PredictionSnapshot(**s)
                    for o in data.get("outcomes", []):
                        self._outcomes[o["outcome_id"]] = OutcomeRecord(**o)
            except Exception as e:
                print(f"Notice: Initializing empty outcome ledger: {e}")

    def _persist(self):
        try:
            os.makedirs(self.ledger_file.parent, exist_ok=True)
            data = {
                "snapshots": [s.model_dump() for s in self._snapshots.values()],
                "outcomes": [o.model_dump() for o in self._outcomes.values()],
                "updated_at": datetime.now().isoformat()
            }
            with open(self.ledger_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to persist outcomes ledger: {e}")

    def save_snapshot(self, snapshot: PredictionSnapshot) -> PredictionSnapshot:
        # Immutable Invariant: once stored, snapshot cannot be rewritten
        if snapshot.prediction_id not in self._snapshots:
            self._snapshots[snapshot.prediction_id] = snapshot
            self._persist()
        return self._snapshots[snapshot.prediction_id]

    def get_snapshot(self, prediction_id: str) -> Optional[PredictionSnapshot]:
        return self._snapshots.get(prediction_id)

    def record_outcome(
        self,
        prediction_id: str,
        user_id: str,
        outcome_status: str,
        user_comment: Optional[str] = None
    ) -> OutcomeRecord:
        """
        Records user-reported event outcome.
        Invariant: Never mutates the original prediction snapshot.
        """
        snapshot = self.get_snapshot(prediction_id)
        outcome_id = f"OUT-{prediction_id[:12]}-{len(self._outcomes) + 1}"
        record = OutcomeRecord(
            outcome_id=outcome_id,
            prediction_id=prediction_id,
            user_id=user_id,
            recorded_at=datetime.now().isoformat(),
            outcome_status=outcome_status,
            user_comment=user_comment,
            is_verified_cohort=bool(snapshot)
        )
        self._outcomes[outcome_id] = record
        self._persist()
        return record

outcome_service = OutcomeService()
