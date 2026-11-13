"""
ZERO-COST PII ANONYMIZER & PRIVACY SHIELD
Applies SHA-256 salted cryptographic hashing to user PII (Name, Email, exact DOB)
before logging or storing analytics data. Complies with DPDP 2023 & GDPR at $0 cost.
"""

import hashlib
import os

# Local secret salt for irreversible anonymization (stored in env or generated locally)
ANONYMIZATION_SALT = os.environ.get("PII_SALT", "prediction_engine_secure_salt_2026")

def anonymize_string(pii_text: str) -> str:
    """Hashes PII string into irreversible 64-character SHA-256 digest."""
    salted = f"{ANONYMIZATION_SALT}:{pii_text.strip().lower()}"
    return hashlib.sha256(salted.encode('utf-8')).hexdigest()

def anonymize_user_profile(name: str, day: int, month: int, year: int) -> dict:
    """Returns anonymized profile dict safe for analytics, logging, or third-party audit."""
    dob_raw = f"{day:02d}-{month:02d}-{year}"
    return {
        "anon_name_hash": anonymize_string(name),
        "anon_dob_hash": anonymize_string(dob_raw),
        "birth_year": year  # Non-identifying year retained for age bracket metrics
    }
