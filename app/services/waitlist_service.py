"""
NUMEROS VISION — DPDP-COMPLIANT ENCRYPTED WAITLIST ("NOTIFY ME") SERVICE
=========================================================================
- Encrypts seeker email using the canonical PII scheme: AES-256-GCM (`ivHex:cipherHex`)
  keyed by a 64-character hex (32-byte) `DATA_ENCRYPTION_KEY`, byte-identical to
  `encryptField` / `decryptField` in `app/static/_worker.js`.
- Retains SHA-256 (`email_sha256`) strictly for de-duplication and delete-on-request lookup.
- Enforces explicit DPDP Act 2023 consent text, stated purpose
  ("tell me when this report is available"), 12-month retention (`expires_at`),
  and immediate delete-on-request erasure.
- Provides `build_waitlist_notification_email` and `produce_waitlist_notifications_for_pack`
  so stored records can deterministically produce outbound availability emails.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import time
from typing import Any, Dict, List, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

WAITLIST_PURPOSE = "tell me when this report is available"
WAITLIST_RETENTION_MONTHS = 12
WAITLIST_RETENTION_SECONDS = 365 * 86400  # 12 months (31,536,000 seconds)
WAITLIST_CONSENT_VERSION = "dpdp_waitlist_v1.0"
DATA_FIDUCIARY_LEGAL_NAME = "Bhaskar Kumar Singh"
DATA_FIDUCIARY_ENTITY = "Numeros Vision Consultancy (Bhaskar Kumar Singh)"
WAITLIST_DPDP_CONSENT_TEXT = (
    'I consent to Numeros Vision storing my encrypted email address for 12 months '
    'solely for the purpose: "tell me when this report is available", with the right '
    'to delete my email record on request at any time under the DPDP Act 2023.'
)

_LOCAL_DEV_FALLBACK_HEX_KEY = (
    "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
)
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_HEX_64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_HEX_24_RE = re.compile(r"^[0-9a-fA-F]{24}$")
_HEX_ANY_RE = re.compile(r"^[0-9a-fA-F]+$")

_PACK_TITLES = {
    "report_advanced": "Anveil my glowing charms (12 Pages)",
    "report_premium": "Anveil every charm (32 Pages)",
}


def default_waitlist_storage_path() -> str:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root_dir, "data", "waitlist_notify_me.jsonl")


def normalize_waitlist_pack_id(pack_id: Optional[str]) -> Optional[str]:
    clean = (pack_id or "").strip().lower()
    if clean in ("report_advanced", "advanced", "report_master", "master"):
        return "report_advanced"
    if clean in ("report_premium", "premium", "report_divine", "divine"):
        return "report_premium"
    return None


def resolve_data_encryption_key(explicit_key: Optional[str] = None) -> str:
    if explicit_key and explicit_key.strip():
        candidate = explicit_key.strip()
    else:
        candidate = (os.getenv("DATA_ENCRYPTION_KEY") or "").strip()

    if candidate:
        parse_32_byte_key(candidate)
        return candidate

    env_mode = (os.getenv("ENVIRONMENT") or "development").strip().lower()
    if env_mode == "production":
        raise RuntimeError(
            "Missing required secret: DATA_ENCRYPTION_KEY (64-character hex 32-byte key required in production)."
        )
    return _LOCAL_DEV_FALLBACK_HEX_KEY


def parse_32_byte_key(secret: str) -> bytes:
    if not secret or not isinstance(secret, str):
        raise ValueError(
            "DATA_ENCRYPTION_KEY is required and must be a 64-character hex (32-byte) key."
        )
    trimmed = secret.strip()
    if not _HEX_64_RE.match(trimmed):
        raise ValueError(
            "DATA_ENCRYPTION_KEY must be a 64-character hex string representing a 32-byte key."
        )
    return bytes.fromhex(trimmed)


def encrypt_pii_field(plain_text: Optional[str], secret: Optional[str] = None) -> Optional[str]:
    """
    Encrypts PII using AES-256-GCM with a random 12-byte IV, returning `ivHex:cipherHex`
    (matching `encryptField` in `app/static/_worker.js`).
    """
    if plain_text is None or plain_text == "":
        return None
    key_bytes = parse_32_byte_key(resolve_data_encryption_key(secret))
    iv = os.urandom(12)
    ct_with_tag = AESGCM(key_bytes).encrypt(iv, str(plain_text).encode("utf-8"), None)
    return f"{iv.hex()}:{ct_with_tag.hex()}"


def decrypt_pii_field(encrypted_text: Optional[str], secret: Optional[str] = None) -> Optional[str]:
    """
    Decrypts `ivHex:cipherHex` produced by `encrypt_pii_field` or Cloudflare Worker `encryptField`.
    """
    if encrypted_text is None or encrypted_text == "":
        return None
    if not isinstance(encrypted_text, str) or ":" not in encrypted_text:
        raise ValueError("Invalid encrypted field format: expected ivHex:cipherHex")
    parts = encrypted_text.split(":")
    if len(parts) != 2:
        raise ValueError("Invalid encrypted field format: expected single colon separator")
    iv_hex, cipher_hex = parts
    if (
        not _HEX_24_RE.match(iv_hex)
        or not _HEX_ANY_RE.match(cipher_hex)
        or len(cipher_hex) < 32
        or len(cipher_hex) % 2 != 0
    ):
        raise ValueError("Invalid encrypted field hex encoding")
    key_bytes = parse_32_byte_key(resolve_data_encryption_key(secret))
    plain_bytes = AESGCM(key_bytes).decrypt(
        bytes.fromhex(iv_hex), bytes.fromhex(cipher_hex), None
    )
    return plain_bytes.decode("utf-8")


def _load_records(storage_path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(storage_path):
        return []
    records: List[Dict[str, Any]] = []
    with open(storage_path, "r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
                if isinstance(obj, dict) and obj.get("email_enc"):
                    records.append(obj)
            except Exception:
                continue
    return records


def _save_records(storage_path: str, records: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(storage_path)), exist_ok=True)
    tmp_path = f"{storage_path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    os.replace(tmp_path, storage_path)


def upsert_waitlist_record(
    email: str,
    pack_id: Optional[str],
    consent: bool,
    purpose: Optional[str] = None,
    consent_text: Optional[str] = None,
    source_page: Optional[str] = "your_reading",
    storage_path: Optional[str] = None,
    encryption_key: Optional[str] = None,
    now_ts: Optional[int] = None,
) -> Dict[str, Any]:
    email_clean = (email or "").strip().lower()
    if not _EMAIL_RE.match(email_clean):
        raise ValueError("Please enter a valid email address.")

    norm_pack = normalize_waitlist_pack_id(pack_id)
    if not norm_pack:
        raise ValueError("Waitlist notifications apply only to Advanced and Premium editions.")

    if consent is not True:
        raise ValueError("Explicit notification consent is required under DPDP 2023.")

    resolved_purpose = (purpose or WAITLIST_PURPOSE).strip()
    if resolved_purpose != WAITLIST_PURPOSE:
        raise ValueError(f'Invalid waitlist purpose; expected "{WAITLIST_PURPOSE}".')

    resolved_consent_text = (consent_text or WAITLIST_DPDP_CONSENT_TEXT).strip()
    if not resolved_consent_text:
        resolved_consent_text = WAITLIST_DPDP_CONSENT_TEXT

    now = int(now_ts if now_ts is not None else time.time())
    expires_at = now + WAITLIST_RETENTION_SECONDS
    email_hash = hashlib.sha256(email_clean.encode("utf-8")).hexdigest()
    email_enc = encrypt_pii_field(email_clean, encryption_key)

    target_path = storage_path or default_waitlist_storage_path()
    existing = [
        r for r in _load_records(target_path) if int(r.get("expires_at") or 0) > now
    ]

    deduplicated = False
    record_id = f"wl_{now}_{secrets.token_hex(4)}"
    updated_records: List[Dict[str, Any]] = []

    for rec in existing:
        if rec.get("email_sha256") == email_hash and rec.get("pack_id") == norm_pack:
            if not deduplicated:
                deduplicated = True
                record_id = str(rec.get("id") or record_id)
                updated_records.append(
                    {
                        "id": record_id,
                        "email_sha256": email_hash,
                        "email_enc": email_enc,
                        "pack_id": norm_pack,
                        "purpose": WAITLIST_PURPOSE,
                        "consent_dpdp": True,
                        "consent_text": resolved_consent_text,
                        "consent_version": WAITLIST_CONSENT_VERSION,
                        "data_fiduciary_legal_name": DATA_FIDUCIARY_LEGAL_NAME,
                        "data_fiduciary": DATA_FIDUCIARY_ENTITY,
                        "retention_months": WAITLIST_RETENTION_MONTHS,
                        "source_page": (source_page or "your_reading")[:64],
                        "created_at": int(rec.get("created_at") or now),
                        "updated_at": now,
                        "expires_at": expires_at,
                    }
                )
        else:
            updated_records.append(rec)

    if not deduplicated:
        updated_records.append(
            {
                "id": record_id,
                "email_sha256": email_hash,
                "email_enc": email_enc,
                "pack_id": norm_pack,
                "purpose": WAITLIST_PURPOSE,
                "consent_dpdp": True,
                "consent_text": resolved_consent_text,
                "consent_version": WAITLIST_CONSENT_VERSION,
                "data_fiduciary_legal_name": DATA_FIDUCIARY_LEGAL_NAME,
                "data_fiduciary": DATA_FIDUCIARY_ENTITY,
                "retention_months": WAITLIST_RETENTION_MONTHS,
                "source_page": (source_page or "your_reading")[:64],
                "created_at": now,
                "updated_at": now,
                "expires_at": expires_at,
            }
        )

    _save_records(target_path, updated_records)

    return {
        "status": "registered",
        "success": True,
        "id": record_id,
        "pack_id": norm_pack,
        "deduplicated": deduplicated,
        "purpose": WAITLIST_PURPOSE,
        "retention_months": WAITLIST_RETENTION_MONTHS,
        "expires_at": expires_at,
        "consent_version": WAITLIST_CONSENT_VERSION,
        "message": (
            "You are on the priority launch list. Your encrypted email is stored for up to "
            "12 months solely to tell you when this report is available, and can be deleted at any time."
        ),
    }


def delete_waitlist_records(
    email: str,
    pack_id: Optional[str] = None,
    storage_path: Optional[str] = None,
) -> Dict[str, Any]:
    email_clean = (email or "").strip().lower()
    if not _EMAIL_RE.match(email_clean):
        raise ValueError("Please enter a valid email address.")

    norm_pack: Optional[str] = None
    if pack_id and str(pack_id).strip():
        norm_pack = normalize_waitlist_pack_id(pack_id)
        if not norm_pack:
            raise ValueError("Invalid pack_id; expected report_advanced or report_premium.")

    email_hash = hashlib.sha256(email_clean.encode("utf-8")).hexdigest()
    target_path = storage_path or default_waitlist_storage_path()
    existing = _load_records(target_path)

    kept: List[Dict[str, Any]] = []
    deleted_count = 0
    for rec in existing:
        matches_email = rec.get("email_sha256") == email_hash
        matches_pack = (norm_pack is None) or (rec.get("pack_id") == norm_pack)
        if matches_email and matches_pack:
            deleted_count += 1
        else:
            kept.append(rec)

    if os.path.exists(target_path) or deleted_count > 0:
        _save_records(target_path, kept)

    return {
        "status": "deleted",
        "success": True,
        "deleted_count": deleted_count,
        "pack_id": norm_pack,
        "message": (
            "Your encrypted email has been permanently deleted from the waitlist."
            if deleted_count > 0
            else "No matching waitlist record was found for that email address."
        ),
    }


def build_waitlist_notification_email(
    record: Dict[str, Any],
    encryption_key: Optional[str] = None,
    now_ts: Optional[int] = None,
) -> Dict[str, str]:
    """
    Produces a complete outbound launch-availability notification email from a stored
    waitlist record by verifying DPDP consent, purpose, and 12-month retention window,
    then decrypting `email_enc`.
    """
    if not isinstance(record, dict):
        raise ValueError("Waitlist record must be a dictionary.")
    if record.get("deleted_at"):
        raise ValueError("Cannot produce notification email for a deleted waitlist record.")
    if record.get("consent_dpdp") is not True:
        raise ValueError("Cannot produce notification email without explicit DPDP consent.")
    if record.get("purpose") != WAITLIST_PURPOSE:
        raise ValueError(
            f'Waitlist record purpose mismatch: expected "{WAITLIST_PURPOSE}".'
        )

    now = int(now_ts if now_ts is not None else time.time())
    expires_at = int(record.get("expires_at") or 0)
    if expires_at <= now:
        raise ValueError("Waitlist record has expired beyond its 12-month retention window.")

    norm_pack = normalize_waitlist_pack_id(record.get("pack_id"))
    if not norm_pack:
        raise ValueError("Waitlist record has unsupported pack_id.")

    email_enc = record.get("email_enc")
    if not email_enc:
        raise ValueError("Waitlist record is missing encrypted email (`email_enc`).")

    recipient = decrypt_pii_field(email_enc, encryption_key)
    if not recipient or not _EMAIL_RE.match(recipient):
        raise ValueError("Decrypted waitlist recipient email is invalid.")

    pack_title = _PACK_TITLES[norm_pack]
    subject = f"{pack_title} Is Now Available | NUMEROS VISION"
    text_body = (
        f"Namaste,\n\n"
        f"You asked us to tell you when {pack_title} becomes available on NUMEROS VISION.\n\n"
        f"This edition is now open at https://numerosvision.com/pricing.html\n\n"
        f"Why you received this email: You provided explicit DPDP 2023 consent for the single purpose "
        f'"{WAITLIST_PURPOSE}" (12-month maximum retention).\n'
        f"To delete your waitlist record at any time, use the Delete Waitlist Email option on our "
        f"Notify Me dialog or contact privacy@numerosvision.com.\n"
        f"Data Fiduciary: {DATA_FIDUCIARY_ENTITY}\n\n"
        f"NUMEROS VISION · ANVEIL EVERY CHARM"
    )
    html_body = (
        f'<div style="font-family:Inter,Arial,sans-serif;background:#FFFDF7;color:#523E28;'
        f'padding:24px;border:1px solid #C9A227;border-radius:12px;max-width:560px;">'
        f'<div style="font-size:12px;letter-spacing:0.12em;color:#8B6914;font-weight:700;">'
        f"NUMEROS VISION · ANVEIL EVERY CHARM</div>"
        f'<h2 style="color:#523E28;margin:10px 0 8px;">{pack_title} Is Now Available</h2>'
        f"<p>You asked us to tell you when <strong>{pack_title}</strong> opens.</p>"
        f'<p><a href="https://numerosvision.com/pricing/" '
        f'style="display:inline-block;padding:10px 18px;background:#8B6914;color:#FFFDF7;'
        f'text-decoration:none;border-radius:8px;font-weight:600;">View Available Report</a></p>'
        f'<p style="font-size:12px;color:#7A654D;margin-top:18px;">'
        f'Sent strictly under your DPDP 2023 consent for purpose: "{WAITLIST_PURPOSE}" '
        f"(12-month retention). Data Fiduciary: {DATA_FIDUCIARY_ENTITY}. "
        f"You may delete your waitlist record on request at any time.</p>"
        f"</div>"
    )

    return {
        "to": recipient,
        "subject": subject,
        "purpose": WAITLIST_PURPOSE,
        "pack_id": norm_pack,
        "text": text_body,
        "html": html_body,
    }


def produce_waitlist_notifications_for_pack(
    pack_id: str,
    storage_path: Optional[str] = None,
    encryption_key: Optional[str] = None,
    now_ts: Optional[int] = None,
) -> List[Dict[str, str]]:
    norm_pack = normalize_waitlist_pack_id(pack_id)
    if not norm_pack:
        raise ValueError("Unsupported waitlist pack_id.")
    now = int(now_ts if now_ts is not None else time.time())
    target_path = storage_path or default_waitlist_storage_path()
    records = _load_records(target_path)

    outbox: List[Dict[str, str]] = []
    for rec in records:
        if rec.get("pack_id") != norm_pack:
            continue
        if int(rec.get("expires_at") or 0) <= now:
            continue
        outbox.append(
            build_waitlist_notification_email(
                rec, encryption_key=encryption_key, now_ts=now
            )
        )
    return outbox
