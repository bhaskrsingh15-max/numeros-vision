"""
NUMEROS VISION — REAL-TIME OTP DISPATCHER SERVICE
Document Version: 1.0.1
Supports dual real-time delivery via:
  1. Real Email via standard SMTP (Gmail App Password, SendGrid, Amazon SES, Brevo, or custom SMTP).
  2. Real Mobile SMS via Fast2SMS (India instant OTP), Twilio (worldwide), or MSG91.
  3. Graceful sandbox fallback with console logging for developer testing.
"""

import os
import smtplib
import ssl
import json
import urllib.request
import urllib.parse
import urllib.error
import re
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def send_real_email_otp(to_email: str, otp_code: str, user_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Delivers a branded, luxury HTML verification email with the 6-digit OTP code.
    Uses TLS/STARTTLS via Python's built-in smtplib.
    """
    # Dynamically read credentials to support live .env updates without server restart
    smtp_host = os.getenv("EMAIL_SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587").strip() or 587)
    smtp_user = os.getenv("EMAIL_SMTP_USER", "").strip()
    smtp_pass = os.getenv("EMAIL_SMTP_PASSWORD", "").strip()
    email_from = os.getenv("EMAIL_FROM", f"Numeros Vision <{smtp_user}>" if smtp_user else "Numeros Vision <support@numerosvision.com>").strip()
    brevo_key = (
        os.getenv("BREVO_API_KEY", "").strip()
        or (
            os.getenv("EMAIL_API_KEY", "").strip()
            if os.getenv("EMAIL_PROVIDER", "").strip().lower() == "brevo"
            or os.getenv("EMAIL_API_KEY", "").strip().startswith("xkeysib-")
            else ""
        )
    )

    clean_email = to_email.strip()
    if not clean_email or "@" not in clean_email:
        return {"delivered": False, "channel": "email", "reason": "Invalid email address format"}

    # If neither Brevo HTTP API nor SMTP is configured, return mock status
    if not brevo_key and (not smtp_host or not smtp_user or not smtp_pass):
        print(f"[OTP_EMAIL_MOCK] Brevo / SMTP not configured in .env for {clean_email}.")
        return {
            "delivered": False,
            "channel": "email",
            "destination": clean_email,
            "reason": "BREVO_API_KEY / EMAIL_API_KEY or EMAIL_SMTP_HOST not set in .env",
            "is_mock": True
        }

    display_name = user_name.strip() if user_name else "Seeker"

    # HTML Email Template with Venus Pearl and Jupiter Gold aesthetics
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <style>
        body {{
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          background-color: #F7F3EA;
          color: #523E28;
          margin: 0;
          padding: 24px;
        }}
        .email-wrapper {{
          max-width: 540px;
          margin: 0 auto;
          background: #FFFDF7;
          border: 1px solid rgba(201, 162, 39, 0.25);
          border-radius: 12px;
          padding: 36px 32px;
          box-shadow: 0 8px 24px rgba(82, 62, 40, 0.06);
        }}
        .brand-header {{
          text-align: center;
          padding-bottom: 24px;
          border-bottom: 1px solid rgba(201, 162, 39, 0.15);
        }}
        .brand-title {{
          font-family: Georgia, serif;
          font-size: 22px;
          letter-spacing: 0.18em;
          color: #8B6914;
          margin: 0 0 4px 0;
          text-transform: uppercase;
        }}
        .brand-tagline {{
          font-size: 11px;
          letter-spacing: 0.25em;
          color: #9E7B15;
          margin: 0;
          text-transform: uppercase;
        }}
        .otp-box {{
          background: linear-gradient(135deg, rgba(201,162,39,0.08), rgba(247,243,234,0.6));
          border: 1.5px dashed #C9A227;
          border-radius: 8px;
          text-align: center;
          padding: 20px 16px;
          margin: 28px 0;
        }}
        .otp-number {{
          font-family: 'SF Mono', Consolas, Monaco, monospace;
          font-size: 36px;
          font-weight: 700;
          letter-spacing: 0.28em;
          color: #8B6914;
          margin: 8px 0;
        }}
        .notice {{
          font-size: 13px;
          line-height: 1.6;
          color: #7A654D;
        }}
        .footer {{
          text-align: center;
          font-size: 11px;
          color: #9E7B15;
          margin-top: 32px;
          border-top: 1px solid rgba(201, 162, 39, 0.15);
          padding-top: 18px;
        }}
      </style>
    </head>
    <body>
      <div class="email-wrapper">
        <div class="brand-header">
          <h1 class="brand-title">NUMEROS VISION</h1>
          <p class="brand-tagline">ANVEIL EVERY CHARM</p>
        </div>

        <p style="font-size: 15px; margin-top: 24px;">Dear {display_name},</p>
        <p class="notice">
          Welcome to Numeros Vision. Use the verification code below to verify your account and calibrate your Golden Profile matrix:
        </p>

        <div class="otp-box">
          <div style="font-size: 12px; letter-spacing: 0.1em; color: #523E28; text-transform: uppercase;">Your 6-Digit Verification Code</div>
          <div class="otp-number">{otp_code}</div>
          <div style="font-size: 11px; color: #9E7B15;">Valid for 10 minutes · Do not share this code with anyone.</div>
        </div>

        <p class="notice">
          If you did not initiate this request, you can safely ignore this email. Your data is protected under India DPDP Act 2023 statutory principles.
        </p>

        <div class="footer">
          © 2026 NUMEROS VISION · ANVEIL EVERY CHARM<br>
          Autonomous High-Precision Numerological Intelligence
        </div>
      </div>
    </body>
    </html>
    """

    text_fallback = f"Your Numeros Vision verification code is {otp_code}. Valid for 10 minutes."

    if brevo_key:
        try:
            sender_email = email_from.split("<")[1].replace(">", "").strip() if "<" in email_from else email_from
            sender_name = email_from.split("<")[0].replace('"', "").replace("'", "").strip() if "<" in email_from else "Numeros Vision"
            payload = json.dumps({
                "sender": {"email": sender_email, "name": sender_name or "Numeros Vision"},
                "to": [{"email": clean_email}],
                "subject": f"Numeros Vision Verification Code: {otp_code}",
                "textContent": text_fallback,
                "htmlContent": html_content,
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.brevo.com/v3/smtp/email",
                data=payload,
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                    "api-key": brevo_key,
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                if 200 <= resp.status < 300:
                    return {
                        "delivered": True,
                        "channel": "email",
                        "provider": "brevo",
                        "destination": clean_email,
                        "message": f"Verification code delivered to {clean_email}",
                    }
        except Exception as e:
            if not (smtp_host and smtp_user and smtp_pass):
                return {"delivered": False, "channel": "email", "provider": "brevo", "destination": clean_email, "error": str(e)}

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Numeros Vision Verification Code: {otp_code}"
        msg["From"] = email_from
        msg["To"] = clean_email

        msg.attach(MIMEText(text_fallback, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        # Connect via SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
            server.ehlo()
            if smtp_port == 587:
                server.starttls(context=context)
                server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, clean_email, msg.as_string())

        print(f"[OTP_EMAIL_SERVICE] Real email successfully sent to {clean_email}")
        return {
            "delivered": True,
            "channel": "email",
            "destination": clean_email,
            "message": f"Verification code delivered to {clean_email}"
        }
    except Exception as e:
        print(f"[OTP_EMAIL_ERROR] Failed to send email to {clean_email}: {e}")
        return {
            "delivered": False,
            "channel": "email",
            "destination": clean_email,
            "error": str(e)
        }


def send_transactional_email_smtp(
    to_email: str,
    subject: str,
    text_body: str,
    html_body: str,
    from_header: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sends a transactional email (e.g. 6-digit OTP or download link) via configured SMTP
    (supports port 465 SSL and port 587 STARTTLS). Never logs OTP content to stdout.
    """
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except Exception:
        pass

    smtp_host = os.getenv("EMAIL_SMTP_HOST", "").strip()
    smtp_port = int((os.getenv("EMAIL_SMTP_PORT", "587") or "587").strip())
    smtp_user = os.getenv("EMAIL_SMTP_USER", "").strip()
    smtp_pass = os.getenv("EMAIL_SMTP_PASSWORD", "").strip()
    email_from = (
        (from_header or "").strip()
        or os.getenv("EMAIL_FROM", "").strip()
        or (f"Numeros Vision <{smtp_user}>" if smtp_user else "Numeros Vision <support@numerosvision.com>")
    )

    clean_email = (to_email or "").strip()
    if not clean_email or "@" not in clean_email:
        return {"delivered": False, "error": "Invalid recipient email address."}

    if not smtp_host or not smtp_user or not smtp_pass:
        return {
            "delivered": False,
            "error": "SMTP credentials are not configured in .env (EMAIL_SMTP_HOST / EMAIL_SMTP_USER / EMAIL_SMTP_PASSWORD missing).",
        }

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = clean_email
        msg.attach(MIMEText(text_body or "", "plain", "utf-8"))
        if html_body:
            msg.attach(MIMEText(html_body, "html", "utf-8"))

        context = ssl.create_default_context()
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=12, context=context) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, [clean_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, [clean_email], msg.as_string())

        return {"delivered": True, "provider": "smtp", "destination": clean_email}
    except Exception as exc:
        return {"delivered": False, "error": f"SMTP dispatch failed: {exc}"}


def _mask_phone_last2(raw_phone: str) -> str:
    digits = re.sub(r"[^0-9]", "", str(raw_phone or ""))
    if len(digits) >= 2:
        return f"+91 ********{digits[-2:]}"
    return "********"


def _redact_sensitive(text: str, otp_code: Optional[str] = None) -> str:
    val = str(text or "")
    if otp_code:
        val = val.replace(str(otp_code), "[REDACTED_OTP]")
    val = re.sub(r"\b\d{6}\b", "[REDACTED_CODE]", val)
    val = re.sub(
        r"\+?\d[\d\s\-()]{7,14}\d",
        lambda m: "********" + re.sub(r"\D", "", m.group(0))[-2:],
        val,
    )
    return val


def _parse_strict_plus91_mobile10(raw_phone: str) -> Optional[str]:
    compact = re.sub(r"[\s\-()]", "", str(raw_phone or "").strip())
    if not compact:
        return None
    m = re.fullmatch(r"(?:\+91|91)?([6-9][0-9]{9})", compact)
    return m.group(1) if m else None


def _is_valid_alphanumeric_sender(raw_sender: str) -> bool:
    return bool(re.fullmatch(r"(?=.*[A-Za-z])[A-Za-z0-9]{3,11}", str(raw_sender or "").strip()))


def send_real_sms_otp(to_phone: str, otp_code: str) -> Dict[str, Any]:
    """
    Delivers transactional OTP SMS via Brevo exclusively for +91 numbers matching ^[6-9][0-9]{9}$.
    Never invents a sender header; skips cleanly when BREVO_SMS_SENDER is unset/invalid.
    Never writes OTP codes or unmasked phone numbers to logs or error payloads.
    """
    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
    except Exception:
        pass

    masked_dest = _mask_phone_last2(to_phone)
    mobile_10 = _parse_strict_plus91_mobile10(to_phone)
    if not mobile_10:
        return {
            "delivered": False,
            "channel": "sms",
            "skipped": True,
            "destination": masked_dest,
            "reason": "invalid_phone",
        }

    raw_sender = (os.getenv("BREVO_SMS_SENDER") or "").strip()
    if not _is_valid_alphanumeric_sender(raw_sender):
        print("sms_skipped: no sender")
        return {
            "delivered": False,
            "channel": "sms",
            "skipped": True,
            "destination": masked_dest,
            "reason": "no_sender",
        }

    brevo_sms_disabled = os.getenv("BREVO_SMS_ENABLED", "").strip().lower() in ("false", "0")
    if brevo_sms_disabled:
        return {
            "delivered": False,
            "channel": "sms",
            "skipped": True,
            "destination": masked_dest,
            "reason": "sms_disabled",
        }

    brevo_key = (
        os.getenv("BREVO_API_KEY", "").strip()
        or (
            os.getenv("EMAIL_API_KEY", "").strip()
            if os.getenv("EMAIL_PROVIDER", "").strip().lower() == "brevo"
            or os.getenv("EMAIL_API_KEY", "").strip().startswith("xkeysib-")
            else ""
        )
    )
    if not brevo_key:
        return {
            "delivered": False,
            "channel": "sms",
            "skipped": True,
            "destination": masked_dest,
            "reason": "brevo_key_missing",
            "is_mock": True,
        }

    tmpl = os.getenv("BREVO_SMS_TEMPLATE", "").strip()
    sms_content = (
        re.sub(r"\{\{?\s*(?:otp|code)\s*\}?\}", str(otp_code), tmpl, flags=re.IGNORECASE)
        if tmpl
        else f"Your Numeros Vision verification code is {otp_code}. Valid for 10 minutes. Do not share this code."
    )
    try:
        payload_dict: Dict[str, Any] = {
            "sender": raw_sender,
            "recipient": f"91{mobile_10}",
            "content": sms_content,
            "type": "transactional",
            "tag": "NumerosVisionOTP",
            "unicodeEnabled": False,
        }
        org_prefix = os.getenv("BREVO_SMS_ORG_PREFIX", "").strip()
        if org_prefix:
            payload_dict["organisationPrefix"] = org_prefix
        payload = json.dumps(payload_dict).encode("utf-8")
        req = urllib.request.Request(
            "https://api.brevo.com/v3/transactionalSMS/send",
            data=payload,
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": brevo_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            if 200 <= resp.status < 300:
                return {
                    "delivered": True,
                    "channel": "sms",
                    "destination": masked_dest,
                    "provider": "brevo",
                }
            return {
                "delivered": False,
                "channel": "sms",
                "destination": masked_dest,
                "provider": "brevo",
                "reason": f"http_{resp.status}",
            }
    except Exception as e:
        return {
            "delivered": False,
            "channel": "sms",
            "destination": masked_dest,
            "provider": "brevo",
            "error": _redact_sensitive(str(e), otp_code),
        }


def dispatch_otp_multichannel(
    phone: Optional[str] = None,
    email: Optional[str] = None,
    otp_code: str = "123456",
    user_name: Optional[str] = None,
    channel: str = "both"
) -> Dict[str, Any]:
    """
    Simultaneously dispatches the OTP code to Mobile SMS and Email inbox.
    Spawns background delivery threads so the API response remains instant.
    """
    results = {}

    def _email_worker():
        if email and ("@" in email):
            res = send_real_email_otp(email, otp_code, user_name)
            results["email"] = res

    def _sms_worker():
        if phone:
            res = send_real_sms_otp(phone, otp_code)
            results["sms"] = res

    threads = []
    if channel in ("email", "both", "auto") and email:
        t1 = threading.Thread(target=_email_worker, daemon=True)
        t1.start()
        threads.append(t1)

    if channel in ("sms", "whatsapp", "both", "auto") and phone:
        t2 = threading.Thread(target=_sms_worker, daemon=True)
        t2.start()
        threads.append(t2)

    # Allow up to 1.5 seconds for quick local dispatch before responding
    for t in threads:
        t.join(timeout=1.5)

    return results
