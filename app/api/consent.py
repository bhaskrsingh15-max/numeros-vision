from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
import time

router = APIRouter(prefix="/api/v1/privacy", tags=["Privacy & Consent Ledger"])

# In-memory consent ledger store for MVP stage (persisted to Postgres schema in production)
CONSENT_LEDGER = []

class ConsentRecord(BaseModel):
    user_id: str
    purpose: str = Field(..., description="Stated purpose (e.g. numerology_reading, remedy_recommendation)")
    granted: bool = Field(..., description="True if granted, False if revoked")

@router.post("/consent")
def update_consent(record: ConsentRecord):
    log_entry = {
        "user_id": record.user_id,
        "purpose": record.purpose,
        "granted": record.granted,
        "timestamp": time.time(),
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    CONSENT_LEDGER.append(log_entry)
    return {
        "status": "success",
        "message": f"Consent recorded for purpose '{record.purpose}'",
        "entry": log_entry
    }

@router.get("/data/{user_id}")
def export_user_data(user_id: str):
    user_logs = [log for log in CONSENT_LEDGER if log["user_id"] == user_id]
    return {
        "status": "success",
        "user_id": user_id,
        "exported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "consent_history": user_logs,
        "pii_retention": "Zero ad-network tracking. Data bound strictly to requested readings."
    }

@router.delete("/data/{user_id}")
def delete_user_data(user_id: str):
    global CONSENT_LEDGER
    CONSENT_LEDGER = [log for log in CONSENT_LEDGER if log["user_id"] != user_id]
    return {
        "status": "success",
        "message": f"All PII and consent records deleted for user '{user_id}' under DPDP/GDPR compliance."
    }
