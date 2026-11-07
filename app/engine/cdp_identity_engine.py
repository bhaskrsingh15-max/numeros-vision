"""
NUMEROS VISION: CDP DETERMINISTIC IDENTITY RESOLUTION & AUDIENCE TAXONOMY ENGINE
Section 15: High-Match Rate 1st-Party Identity Graph, Normalization & Dual Taxonomy.

Features:
1. Deterministic Normalization & SHA-256 Hashing:
   - Phone: E.164 normalization (+919876543210 -> stripped -> SHA-256)
   - Email: RFC-5322 normalization, lowercase, trimmed, Gmail dot/plus removal -> SHA-256
   - Device/Ad IDs: GAID/AAID (Android), IDFA (iOS with ATT consent), 1P Cookie (_nv_uid)
2. Identity Graph Merger:
   - Links anonymous web sessions, email lead captures, and payment phone numbers into a single Golden Profile ID.
3. Dual-Layer Audience Taxonomy:
   - Deterministic Taxonomy: Verified Mulank, Bhagyank, Lagna, Active Dasha, Purchase Tier.
   - Probabilistic Taxonomy: Career Pivot Intent, Marriage Urgency, Transit Friction Index, HNI Affluence Score.
4. AdTech Activation Formatters:
   - Meta CAPI (Conversions API) High-Match Payload (Targeting 8.5+ Event Match Quality).
   - Google Enhanced Conversions Payload.
"""

import re
import uuid
import time
import hashlib
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# ── 1. DETERMINISTIC NORMALIZATION & HASHING ─────────────────────────────────

def normalize_email(raw_email: str) -> str:
    """Normalizes email according to Meta/Google Enhanced Conversions specs:
       trimmed, lowercase, gmail dot removal, sub-address (plus) stripping."""
    if not raw_email:
        return ""
    clean = raw_email.strip().lower()
    parts = clean.split("@")
    if len(parts) != 2:
        return clean
    user, domain = parts
    # Gmail specific normalization
    if domain in ("gmail.com", "googlemail.com"):
        user = user.replace(".", "")
        user = user.split("+")[0]
    else:
        user = user.split("+")[0]
    return f"{user}@{domain}"

def normalize_phone(raw_phone: str, default_country_code: str = "91") -> str:
    """Normalizes phone number to E.164 without leading '+' or special chars:
       e.g., '+91 98765-43210' -> '919876543210'."""
    if not raw_phone:
        return ""
    # Strip all non-digit characters
    digits = re.sub(r"\D", "", raw_phone)
    # Handle leading zeros
    digits = digits.lstrip("0")
    # If 10 digits and default is India, prepend 91
    if len(digits) == 10 and default_country_code:
        digits = f"{default_country_code}{digits}"
    return digits

def hash_sha256(normalized_val: str) -> str:
    """Generates standard lowercased hex SHA-256 hash required by Ad Platforms."""
    if not normalized_val:
        return ""
    return hashlib.sha256(normalized_val.encode("utf-8")).hexdigest()


# ── 2. IDENTITY GRAPH STORE (IN-MEMORY / POSTGRES SCHEMA) ────────────────────

# In-memory identity graph tables: {identifier_hash: golden_profile_id}
_IDENTIFIER_TO_GOLDEN_ID: Dict[str, str] = {}
# {golden_profile_id: GoldenProfile}
_GOLDEN_PROFILES: Dict[str, Dict[str, Any]] = {}

class IdentityPayload(BaseModel):
    # Deterministic Identifiers
    email: Optional[str] = Field(None, description="Plaintext email for hashing")
    phone: Optional[str] = Field(None, description="Plaintext phone for E.164 hashing")
    # Mobile & Tablet Advertising Identifiers
    gaid_aaid: Optional[str] = Field(None, description="Google Advertising ID (Android - Mobile/Tablet)")
    idfa: Optional[str] = Field(None, description="Apple IDFA (iOS/iPadOS - with ATT consent)")
    idfv: Optional[str] = Field(None, description="Apple IDFV (Identifier for Vendors - iOS/iPadOS)")
    # Device Identifiers across Mobile, Tablet & Desktop
    device_id: Optional[str] = Field(None, description="1st-party persistent Device ID / App Set ID / Web Client UUID")
    device_type: Optional[str] = Field("desktop", description="Device form factor: mobile, tablet, or desktop")
    # First-Party Web / Session Identifiers
    nv_uid: Optional[str] = Field(None, description="1st-party persistent cookie ID")
    fbp: Optional[str] = Field(None, description="Meta _fbp browser cookie")
    fbc: Optional[str] = Field(None, description="Meta _fbc click ID (fbclid)")
    gclid: Optional[str] = Field(None, description="Google Click Identifier")
    client_ip: Optional[str] = Field(None, description="Client IPv4/IPv6 for server match")
    client_user_agent: Optional[str] = Field(None, description="Client browser User Agent")
    # Consent Flags (India DPDP Act 2023 / GDPR / Apple ATT)
    consent_marketing: bool = Field(True, description="Opt-in consent for ad personalization")
    consent_device_tracking: bool = Field(True, description="Explicit user consent for device and advertising identifier capture")


def resolve_golden_profile(payload: IdentityPayload) -> Dict[str, Any]:
    """
    Deterministically resolves multiple fragmented identifiers into a unified Golden Customer Profile.
    If any single identifier matches an existing record, the graph links all other identifiers to it.
    Complies with DPDP Act 2023 / GDPR / Apple ATT: only indexes device and advertising IDs if consent is granted.
    """
    norm_email = normalize_email(payload.email) if payload.email else ""
    norm_phone = normalize_phone(payload.phone) if payload.phone else ""
    
    email_hash = hash_sha256(norm_email)
    phone_hash = hash_sha256(norm_phone)
    
    # Handle Device and Ad IDs with Consent Guard
    device_consent = payload.consent_device_tracking and payload.consent_marketing
    gaid_val = (payload.gaid_aaid.strip().lower() if payload.gaid_aaid else "") if device_consent else ""
    idfa_val = (payload.idfa.strip().lower() if (payload.idfa and payload.idfa != "00000000-0000-0000-0000-000000000000") else "") if device_consent else ""
    idfv_val = (payload.idfv.strip().lower() if payload.idfv else "") if device_consent else ""
    device_id_val = (payload.device_id.strip() if payload.device_id else "") if device_consent else ""
    device_type_val = payload.device_type.strip().lower() if payload.device_type else "desktop"
    nv_uid_val = payload.nv_uid.strip() if payload.nv_uid else ""

    # Keys used for deterministic matching
    keys_to_check = [k for k in [
        f"email:{email_hash}" if email_hash else None,
        f"phone:{phone_hash}" if phone_hash else None,
        f"gaid:{gaid_val}" if gaid_val else None,
        f"idfa:{idfa_val}" if idfa_val else None,
        f"idfv:{idfv_val}" if idfv_val else None,
        f"device_id:{device_id_val}" if device_id_val else None,
        f"1p_uid:{nv_uid_val}" if nv_uid_val else None
    ] if k]

    existing_golden_id = None
    for key in keys_to_check:
        if key in _IDENTIFIER_TO_GOLDEN_ID:
            existing_golden_id = _IDENTIFIER_TO_GOLDEN_ID[key]
            break

    # If no existing profile, mint a new Golden Profile ID
    golden_id = existing_golden_id or f"gp_{uuid.uuid4().hex[:16]}"

    if golden_id not in _GOLDEN_PROFILES:
        _GOLDEN_PROFILES[golden_id] = {
            "golden_profile_id": golden_id,
            "created_at": time.time(),
            "updated_at": time.time(),
            "hashes": {},
            "ad_ids": {},
            "devices": {},
            "cookies": {},
            "deterministic_taxonomy": {},
            "probabilistic_taxonomy": {},
            "consent_status": payload.consent_marketing,
            "consent_device_tracking": payload.consent_device_tracking
        }

    profile = _GOLDEN_PROFILES[golden_id]
    profile["updated_at"] = time.time()
    profile["consent_status"] = payload.consent_marketing
    profile["consent_device_tracking"] = payload.consent_device_tracking

    # Ensure container keys exist
    if "devices" not in profile:
        profile["devices"] = {}
    if "ad_ids" not in profile:
        profile["ad_ids"] = {}

    # Store hashes
    if email_hash:
        profile["hashes"]["email_sha256"] = email_hash
    if phone_hash:
        profile["hashes"]["phone_sha256"] = phone_hash
    
    # Store Ad IDs (only if consent granted)
    if gaid_val:
        profile["ad_ids"]["gaid"] = gaid_val
    if idfa_val:
        profile["ad_ids"]["idfa"] = idfa_val
    if idfv_val:
        profile["ad_ids"]["idfv"] = idfv_val
        
    # Store Device Metadata
    if device_id_val or device_type_val:
        profile["devices"]["primary_device_id"] = device_id_val or profile["devices"].get("primary_device_id", "")
        profile["devices"]["device_type"] = device_type_val
        profile["devices"]["platform_family"] = "mobile" if device_type_val == "mobile" else ("tablet" if device_type_val == "tablet" else "desktop")

    # Store Cookies / Web attribution
    if nv_uid_val:
        profile["cookies"]["nv_uid"] = nv_uid_val
    if payload.fbp:
        profile["cookies"]["_fbp"] = payload.fbp
    if payload.fbc:
        profile["cookies"]["_fbc"] = payload.fbc
    if payload.gclid:
        profile["cookies"]["gclid"] = payload.gclid
    if payload.client_ip:
        profile["cookies"]["client_ip"] = payload.client_ip
    if payload.client_user_agent:
        profile["cookies"]["client_user_agent"] = payload.client_user_agent

    # Update index map for all keys
    for key in keys_to_check:
        _IDENTIFIER_TO_GOLDEN_ID[key] = golden_id

    return profile


# ── 3. DUAL-LAYER AUDIENCE TAXONOMY GENERATOR ────────────────────────────────

def enrich_audience_taxonomy(
    golden_profile_id: str,
    chart_data: Dict[str, Any],
    transaction_data: Optional[Dict[str, Any]] = None,
    behavioral_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Enriches the Golden Customer Profile with both:
    1. Deterministic Taxonomy (Verified birth data, Dasha, Mulank, Bhagyank, Spend tier).
    2. Probabilistic Taxonomy (Predictive intent scores, transit friction index, HNI propensity).
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile:
        raise ValueError(f"Golden Profile {golden_profile_id} does not exist.")

    # A. DETERMINISTIC TAXONOMY ENRICHMENT
    det = {}
    det["astro_sun_sign"] = chart_data.get("sun_sign", "Unknown")
    det["astro_moon_sign"] = chart_data.get("moon_sign", "Unknown")
    det["astro_lagna"] = chart_data.get("lagna", "Unknown")
    det["numerology_mulank"] = chart_data.get("mulank", 0)
    det["numerology_bhagyank"] = chart_data.get("bhagyank", 0)
    det["active_mahadasha"] = chart_data.get("mahadasha", "Unknown")
    det["active_antardasha"] = chart_data.get("antardasha", "Unknown")
    det["lo_shu_missing"] = chart_data.get("missing_numbers", [])
    
    # Financial / Tier Attributes
    tx = transaction_data or {}
    total_spend = tx.get("total_spend_inr", 0)
    det["purchase_count"] = tx.get("purchase_count", 0)
    det["total_spend_inr"] = total_spend
    
    if total_spend >= 4999:
        det["customer_tier"] = "HNI_CONSULTATION_CLIENT"
    elif total_spend >= 499:
        det["customer_tier"] = "MASTER_REPORT_BUYER"
    elif total_spend >= 99:
        det["customer_tier"] = "ENTRY_TRIAL_BUYER"
    else:
        det["customer_tier"] = "FREE_SCORECARD_LEAD"

    profile["deterministic_taxonomy"] = det

    # B. PROBABILISTIC (PREDICTIVE) TAXONOMY ENRICHMENT
    prob = {}
    beh = behavioral_data or {}
    
    # 1. Career Pivot Propensity (0.0 to 1.0)
    # Calculated from 10th house Dasha activation + page views on Career report / tool
    career_views = beh.get("page_views_career", 0)
    dasha_career_affinity = 1.0 if det["active_mahadasha"] in ["Saturn", "Sun", "Mercury", "Jupiter"] else 0.4
    prob["career_pivot_propensity"] = round(min(1.0, (career_views * 0.2) + (dasha_career_affinity * 0.5)), 2)

    # 2. Marriage & Relationship Urgency (0.0 to 1.0)
    # Calculated from 7th house / Venus / Jupiter activation + love calculator usage
    love_views = beh.get("page_views_love", 0)
    dasha_love_affinity = 1.0 if det["active_mahadasha"] in ["Venus", "Jupiter", "Moon"] else 0.3
    prob["marriage_urgency_propensity"] = round(min(1.0, (love_views * 0.25) + (dasha_love_affinity * 0.5)), 2)

    # 3. Transit Friction / Remedy Purchase Intent (0.0 to 1.0)
    # If Saturn/Rahu transit is afflicting natal Moon or Lagna -> High remedy propensity
    is_saturn_challenging = chart_data.get("is_saturn_challenging", False)
    is_rahu_challenging = chart_data.get("is_rahu_challenging", False)
    remedy_score = 0.3
    if is_saturn_challenging: remedy_score += 0.35
    if is_rahu_challenging: remedy_score += 0.25
    prob["transit_friction_index"] = round(min(1.0, remedy_score), 2)

    # 4. HNI Affluence Propensity Score (0.0 to 1.0)
    # Inferred from device model (e.g. iPhone Pro), high-ticket consultation clicks
    device = profile.get("cookies", {}).get("client_user_agent", "").lower()
    is_premium_device = any(d in device for d in ["iphone", "macintosh", "ipad"])
    viewed_corporate = beh.get("viewed_business_consultation", False)
    affluence = 0.4
    if is_premium_device: affluence += 0.3
    if viewed_corporate: affluence += 0.3
    prob["hni_affluence_propensity"] = round(min(1.0, affluence), 2)

    profile["probabilistic_taxonomy"] = prob
    return profile


def enrich_deterministic_taxonomy(golden_profile_id: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Specifically enriches or updates Deterministic Audience Taxonomy attributes separately.
    Attributes include: mulank, bhagyank, sun_sign, moon_sign, lagna, mahadasha, antardasha,
    lo_shu_missing, customer_tier, total_spend_inr, purchase_count, name_expression_number, soul_urge_number.
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile:
        raise ValueError(f"Golden Profile {golden_profile_id} does not exist.")
    
    if "deterministic_taxonomy" not in profile:
        profile["deterministic_taxonomy"] = {}
    
    det = profile["deterministic_taxonomy"]
    for k, v in attributes.items():
        det[k] = v
        
    # Re-evaluate customer tier if spend updated
    if "total_spend_inr" in attributes:
        spend = float(attributes["total_spend_inr"])
        if spend >= 4999:
            det["customer_tier"] = "HNI_CONSULTATION_CLIENT"
        elif spend >= 499:
            det["customer_tier"] = "MASTER_REPORT_BUYER"
        elif spend >= 99:
            det["customer_tier"] = "ENTRY_TRIAL_BUYER"
        else:
            det["customer_tier"] = "FREE_SCORECARD_LEAD"
            
    profile["updated_at"] = time.time()
    return det


def enrich_probabilistic_taxonomy(golden_profile_id: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Specifically enriches or updates Probabilistic Audience Taxonomy attributes separately.
    Attributes include predictive scores (0.0 to 1.0): career_pivot_propensity, marriage_urgency_propensity,
    transit_friction_index, hni_affluence_propensity, gemstone_remedy_readiness, retention_affinity_score.
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile:
        raise ValueError(f"Golden Profile {golden_profile_id} does not exist.")
        
    if "probabilistic_taxonomy" not in profile:
        profile["probabilistic_taxonomy"] = {}
        
    prob = profile["probabilistic_taxonomy"]
    for k, v in attributes.items():
        # Ensure values are rounded floats between 0.0 and 1.0
        try:
            val = round(max(0.0, min(1.0, float(v))), 2)
            prob[k] = val
        except (ValueError, TypeError):
            prob[k] = v
            
    profile["updated_at"] = time.time()
    return prob


def _format_taxonomy_lookup_response(profile: Dict[str, Any], matched_by: str) -> Dict[str, Any]:
    """Formats full omnichannel profile with cleanly separated taxonomies and mapped identifiers."""
    gid = profile["golden_profile_id"]
    det = profile.get("deterministic_taxonomy", {})
    prob = profile.get("probabilistic_taxonomy", {})
    hashes = profile.get("hashes", {})
    devices = profile.get("devices", {})
    ad_ids = profile.get("ad_ids", {})
    cookies = profile.get("cookies", {})
    
    return {
        "status": "success",
        "golden_profile_id": gid,
        "matched_by": matched_by,
        "consent_status": profile.get("consent_status", True),
        "consent_device_tracking": profile.get("consent_device_tracking", True),
        "mapped_identifiers": {
            "email_sha256": hashes.get("email_sha256", "Not linked"),
            "phone_sha256": hashes.get("phone_sha256", "Not linked"),
            "primary_device_id": devices.get("primary_device_id", "Not recorded"),
            "device_type": devices.get("device_type", "desktop"),
            "platform_family": devices.get("platform_family", "desktop"),
            "gaid": ad_ids.get("gaid", "None"),
            "idfa": ad_ids.get("idfa", "None"),
            "idfv": ad_ids.get("idfv", "None"),
            "nv_uid": cookies.get("nv_uid", "None"),
            "_fbp": cookies.get("_fbp", "None"),
            "gclid": cookies.get("gclid", "None")
        },
        "deterministic_taxonomy": {
            "numerology_mulank": det.get("numerology_mulank", 0),
            "numerology_bhagyank": det.get("numerology_bhagyank", 0),
            "astro_sun_sign": det.get("astro_sun_sign", "Unknown"),
            "astro_moon_sign": det.get("astro_moon_sign", "Unknown"),
            "astro_lagna": det.get("astro_lagna", "Unknown"),
            "active_mahadasha": det.get("active_mahadasha", "Unknown"),
            "active_antardasha": det.get("active_antardasha", "Unknown"),
            "lo_shu_missing": det.get("lo_shu_missing", []),
            "customer_tier": det.get("customer_tier", "FREE_SCORECARD_LEAD"),
            "total_spend_inr": det.get("total_spend_inr", 0.0),
            "purchase_count": det.get("purchase_count", 0),
            "name_expression_number": det.get("name_expression_number", det.get("numerology_mulank", 1)),
            "soul_urge_number": det.get("soul_urge_number", 1)
        },
        "probabilistic_taxonomy": {
            "career_pivot_propensity": prob.get("career_pivot_propensity", 0.0),
            "marriage_urgency_propensity": prob.get("marriage_urgency_propensity", 0.0),
            "transit_friction_index": prob.get("transit_friction_index", 0.0),
            "hni_affluence_propensity": prob.get("hni_affluence_propensity", 0.0),
            "gemstone_remedy_readiness": prob.get("gemstone_remedy_readiness", round(prob.get("transit_friction_index", 0.3) * 0.9, 2)),
            "retention_affinity_score": prob.get("retention_affinity_score", 0.85 if det.get("total_spend_inr", 0) > 0 else 0.45)
        },
        "meta_capi_ready": bool(hashes.get("email_sha256") or hashes.get("phone_sha256")),
        "uid2_token": generate_uid2_token(gid),
        "iab_sda_segments": build_iab_sda_user_data(gid)
    }


def lookup_taxonomy_by_any_identifier(query: str, query_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Looks up and returns the separated Deterministic and Probabilistic Taxonomy mapped 
    to ANY identifier:
    - Mobile / WhatsApp Number (e.g. '+919876543210', '9876543210')
    - Email ID (e.g. 'anand@example.com')
    - Device ID (e.g. 'nv_dev_ios_48b1', 'nv_dev_desk_7710')
    - Advertising ID: Android GAID (UUID) or Apple IDFA / IDFV
    - SHA-256 Hash of Email or Phone
    - Golden Profile ID ('gp_...')
    """
    if not query:
        return None
    raw = query.strip()
    clean_lower = raw.lower()
    
    # 1. Direct Golden ID match
    if raw in _GOLDEN_PROFILES:
        return _format_taxonomy_lookup_response(_GOLDEN_PROFILES[raw], f"golden_id:{raw}")
        
    candidates = []
    
    # Email detection
    if "@" in raw or query_type == "email":
        norm_em = normalize_email(raw)
        em_hash = hash_sha256(norm_em)
        candidates.append((f"email:{em_hash}", f"email:{norm_em}"))
        
    # Phone detection (digits)
    digits = re.sub(r"\D", "", raw)
    if (len(digits) >= 10 and ("+" in raw or digits.startswith("91") or len(digits) == 10)) or query_type == "phone":
        norm_ph = normalize_phone(raw)
        ph_hash = hash_sha256(norm_ph)
        candidates.append((f"phone:{ph_hash}", f"phone:+{norm_ph}"))
        
    # 64-char hex hash
    if len(raw) == 64 and all(c in "0123456789abcdefABCDEF" for c in raw):
        candidates.append((f"email:{clean_lower}", "email_sha256"))
        candidates.append((f"phone:{clean_lower}", "phone_sha256"))
        
    # Device ID
    candidates.append((f"device_id:{raw}", f"device_id:{raw}"))
    # Advertising IDs
    candidates.append((f"gaid:{clean_lower}", f"gaid:{clean_lower}"))
    candidates.append((f"idfa:{clean_lower}", f"idfa:{clean_lower}"))
    candidates.append((f"idfv:{clean_lower}", f"idfv:{clean_lower}"))
    # 1P cookie
    candidates.append((f"1p_uid:{raw}", f"1p_uid:{raw}"))
    
    for key, matched_label in candidates:
        if key in _IDENTIFIER_TO_GOLDEN_ID:
            gid = _IDENTIFIER_TO_GOLDEN_ID[key]
            if gid in _GOLDEN_PROFILES:
                return _format_taxonomy_lookup_response(_GOLDEN_PROFILES[gid], matched_label)
                
    return None


def sync_omnichannel_taxonomy(
    email: Optional[str] = None,
    phone: Optional[str] = None,
    device_id: Optional[str] = None,
    device_type: str = "desktop",
    gaid_aaid: Optional[str] = None,
    idfa: Optional[str] = None,
    idfv: Optional[str] = None,
    nv_uid: Optional[str] = None,
    deterministic_attributes: Optional[Dict[str, Any]] = None,
    probabilistic_attributes: Optional[Dict[str, Any]] = None,
    consent_marketing: bool = True,
    consent_device_tracking: bool = True
) -> Dict[str, Any]:
    """
    Synchronizes and bi-directionally maps Mobile Number, Email ID, Device ID, and Advertising IDs
    into a unified Golden Profile, enriching Deterministic and Probabilistic Audience Taxonomies separately.
    """
    payload = IdentityPayload(
        email=email,
        phone=phone,
        device_id=device_id,
        device_type=device_type,
        gaid_aaid=gaid_aaid,
        idfa=idfa,
        idfv=idfv,
        nv_uid=nv_uid,
        consent_marketing=consent_marketing,
        consent_device_tracking=consent_device_tracking
    )
    profile = resolve_golden_profile(payload)
    gid = profile["golden_profile_id"]
    
    # 1. Enrich Deterministic Attributes separately if provided
    if deterministic_attributes:
        enrich_deterministic_taxonomy(gid, deterministic_attributes)
        
    # 2. Enrich Probabilistic Attributes separately if provided
    if probabilistic_attributes:
        enrich_probabilistic_taxonomy(gid, probabilistic_attributes)
        
    return _format_taxonomy_lookup_response(profile, "omnichannel_sync")


# ── 4. HIGH-MATCH RATE ADTECH ACTIVATION FORMATTERS ──────────────────────────

def build_meta_capi_payload(
    golden_profile_id: str,
    event_name: str,
    event_id: str,
    event_source_url: str,
    value: float = 0.0,
    currency: str = "INR"
) -> Dict[str, Any]:
    """
    Constructs a Meta Conversions API (CAPI) payload meeting the 8.5+ Event Match Quality (EMQ) benchmark:
    Includes hashed email, hashed phone, fbp, fbc, IP, user-agent, external_id.
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile or not profile.get("consent_status", False):
        return {}

    hashes = profile.get("hashes", {})
    cookies = profile.get("cookies", {})

    user_data = {
        "external_id": [hash_sha256(golden_profile_id)]
    }
    if "email_sha256" in hashes:
        user_data["em"] = [hashes["email_sha256"]]
    if "phone_sha256" in hashes:
        user_data["ph"] = [hashes["phone_sha256"]]
    if "_fbp" in cookies:
        user_data["fbp"] = cookies["_fbp"]
    if "_fbc" in cookies:
        user_data["fbc"] = cookies["_fbc"]
    if "client_ip" in cookies:
        user_data["client_ip_address"] = cookies["client_ip"]
    if "client_user_agent" in cookies:
        user_data["client_user_agent"] = cookies["client_user_agent"]

    payload = {
        "data": [
            {
                "event_name": event_name,
                "event_time": int(time.time()),
                "event_id": event_id,
                "event_source_url": event_source_url,
                "action_source": "website",
                "user_data": user_data,
                "custom_data": {
                    "currency": currency,
                    "value": value,
                    "customer_tier": profile.get("deterministic_taxonomy", {}).get("customer_tier", "FREE"),
                    "transit_friction": profile.get("probabilistic_taxonomy", {}).get("transit_friction_index", 0.0)
                }
            }
        ]
    }
    return payload


# ── 5. IAB TECH LAB AUDIENCE TAXONOMY & SELLER-DEFINED AUDIENCES (SDA) ──────

# Official IAB Tech Lab Audience Taxonomy (v1.1 / v1.2 / Curated Audiences) Mapping
IAB_AUDIENCE_TAXONOMY_MAP = {
    # ── Life Events & Transitional Cohorts
    "career_transition": {
        "iab_id": "137",
        "name": "Life Events > Career Transition / Job Change",
        "segtax": 4
    },
    "moving_relocation": {
        "iab_id": "138",
        "name": "Life Events > Moving / Relocation",
        "segtax": 4
    },
    "newly_engaged_marriage": {
        "iab_id": "139",
        "name": "Life Events > Newly Engaged / Married",
        "segtax": 4
    },
    "purchasing_home": {
        "iab_id": "140",
        "name": "Life Events > Purchasing a Home",
        "segtax": 4
    },
    # ── In-Market / Purchase Intent
    "in_market_jewelry_luxury": {
        "iab_id": "648",
        "name": "Purchase Intent > Apparel & Accessories > Jewelry & Watches",
        "segtax": 4
    },
    "in_market_real_estate": {
        "iab_id": "712",
        "name": "Purchase Intent > Real Estate > Residential Properties",
        "segtax": 4
    },
    "in_market_wealth_investment": {
        "iab_id": "782",
        "name": "Purchase Intent > Financial Services > Investment & Wealth Management",
        "segtax": 4
    },
    "in_market_holistic_wellness": {
        "iab_id": "831",
        "name": "Purchase Intent > Health & Wellness > Alternative Medicine & Holistic Health",
        "segtax": 4
    },
    # ── Demographics & Affluence
    "demographic_affluent_hni": {
        "iab_id": "52",
        "name": "Demographics > Household Income > High Net Worth / Affluent",
        "segtax": 4
    },
    "demographic_single_seeking": {
        "iab_id": "12",
        "name": "Demographics > Marital Status > Single / Unmarried",
        "segtax": 4
    },
    "demographic_married": {
        "iab_id": "14",
        "name": "Demographics > Marital Status > Married",
        "segtax": 4
    }
}


def build_iab_sda_user_data(golden_profile_id: str) -> Dict[str, Any]:
    """
    Constructs an IAB Seller-Defined Audiences (Curated Audiences) OpenRTB 2.5/2.6
    `user.data` block to monetize first-party astrological & numerological cohorts
    programmatically across DSPs (The Trade Desk, DV360, Amazon DSP, Criteo)
    without third-party cookies.
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile or not profile.get("consent_status", False):
        return {}

    det = profile.get("deterministic_taxonomy", {})
    prob = profile.get("probabilistic_taxonomy", {})

    segments = []

    # Map Career Pivot Propensity
    if prob.get("career_pivot_propensity", 0.0) >= 0.70:
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["career_transition"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["career_transition"]["name"]
        })

    # Map Marriage / Relationship Urgency
    if prob.get("marriage_urgency_propensity", 0.0) >= 0.70:
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["newly_engaged_marriage"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["newly_engaged_marriage"]["name"]
        })
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["in_market_jewelry_luxury"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["in_market_jewelry_luxury"]["name"]
        })

    # Map HNI Affluence
    if prob.get("hni_affluence_propensity", 0.0) >= 0.70 or det.get("customer_tier") == "HNI_CONSULTATION_CLIENT":
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["demographic_affluent_hni"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["demographic_affluent_hni"]["name"]
        })
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["in_market_wealth_investment"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["in_market_wealth_investment"]["name"]
        })

    # Map Holistic Health / Transit Friction
    if prob.get("transit_friction_index", 0.0) >= 0.65:
        segments.append({
            "id": IAB_AUDIENCE_TAXONOMY_MAP["in_market_holistic_wellness"]["iab_id"],
            "name": IAB_AUDIENCE_TAXONOMY_MAP["in_market_holistic_wellness"]["name"]
        })

    if not segments:
        return {}

    return {
        "name": "numerosvision.com",
        "segment": segments,
        "ext": {
            "segtax": 4,  # IAB Tech Lab Audience Taxonomy v1.1 / Curated Audiences
            "provenance": "1st_party_deterministic_and_probabilistic_astro_signals"
        }
    }


def generate_uid2_token(golden_profile_id: str) -> Optional[str]:
    """
    Generates a simulated Unified ID 2.0 (UID2) advertising token from the
    normalized email/phone hash under IAB Tech Lab UID2 open-source standards.
    """
    profile = _GOLDEN_PROFILES.get(golden_profile_id)
    if not profile or not profile.get("consent_status", False):
        return None

    hashes = profile.get("hashes", {})
    primary_hash = hashes.get("email_sha256") or hashes.get("phone_sha256")
    if not primary_hash:
        return None

    # UID2 Token format: base64-like pseudorandom string with version header
    uid2_secret_salt = "NV_UID2_SALT_KEY_2026"
    raw_token = hashlib.sha256(f"{uid2_secret_salt}:{primary_hash}:{int(time.time() / 86400)}".encode("utf-8")).hexdigest()
    return f"UID2_v2_{raw_token[:32]}"



# ── 5. SEED ENTERPRISE AUDIENCE ARCHETYPES (INITIAL STATE) ───────────────────
def ensure_seed_golden_profiles():
    """Initializes high-fidelity deterministic and probabilistic cohorts if store is empty."""
    if len(_GOLDEN_PROFILES) >= 5:
        return

    sample_seed_users = [
        {
            "name": "Vikramaditya Singhania",
            "email": "vikram.singhania@corp.in",
            "phone": "+91 98200 11223",
            "device_id": "nv_dev_ios_pro_101",
            "device_type": "mobile",
            "idfa": "ea7583cd-a667-48bc-b806-42ecb2b48d12",
            "chart": {"mulank": 1, "bhagyank": 1, "mahadasha": "Sun", "antardasha": "Mars", "sun_sign": "Leo"},
            "tx": {"total_spend_inr": 4999.0, "purchase_count": 2},
            "beh": {"page_views_career": 12, "viewed_business_consultation": True}
        },
        {
            "name": "Priyanka Deshmukh",
            "email": "priyanka.d@outlook.com",
            "phone": "+91 98765 43210",
            "device_id": "nv_dev_desk_7710",
            "device_type": "desktop",
            "chart": {"mulank": 5, "bhagyank": 6, "mahadasha": "Mercury", "antardasha": "Venus", "sun_sign": "Gemini"},
            "tx": {"total_spend_inr": 510.0, "purchase_count": 1},
            "beh": {"page_views_career": 6, "page_views_love": 2}
        },
        {
            "name": "Ananya Sen",
            "email": "ananya.sen@gmail.com",
            "phone": "+91 97110 55443",
            "device_id": "nv_dev_tab_9921",
            "device_type": "tablet",
            "gaid_aaid": "38400000-8cf0-11bd-b23e-10b96e40000d",
            "chart": {"mulank": 2, "bhagyank": 7, "mahadasha": "Moon", "antardasha": "Jupiter", "is_saturn_challenging": True},
            "tx": {"total_spend_inr": 199.0, "purchase_count": 1},
            "beh": {"page_views_career": 3, "page_views_love": 8}
        },
        {
            "name": "Rajeshwari Iyer",
            "email": "r.iyer@fintech.co",
            "phone": "+91 99887 76655",
            "device_id": "nv_dev_mob_s24_88",
            "device_type": "mobile",
            "gaid_aaid": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
            "chart": {"mulank": 8, "bhagyank": 4, "mahadasha": "Saturn", "antardasha": "Rahu", "is_saturn_challenging": True, "is_rahu_challenging": True},
            "tx": {"total_spend_inr": 4999.0, "purchase_count": 3},
            "beh": {"page_views_career": 15, "viewed_business_consultation": True}
        },
        {
            "name": "Kabir Mehta",
            "email": "kabir.mehta@studio.design",
            "phone": "+91 98450 33221",
            "device_id": "nv_dev_mac_m3_42",
            "device_type": "desktop",
            "chart": {"mulank": 6, "bhagyank": 9, "mahadasha": "Venus", "antardasha": "Mars", "sun_sign": "Taurus"},
            "tx": {"total_spend_inr": 510.0, "purchase_count": 1},
            "beh": {"page_views_career": 4, "viewed_business_consultation": True}
        }
    ]

    for u in sample_seed_users:
        p = resolve_golden_profile(IdentityPayload(
            email=u["email"],
            phone=u["phone"],
            device_id=u.get("device_id"),
            device_type=u.get("device_type", "desktop"),
            idfa=u.get("idfa"),
            gaid_aaid=u.get("gaid_aaid"),
            consent_marketing=True,
            consent_device_tracking=True
        ))
        enrich_audience_taxonomy(
            p["golden_profile_id"],
            chart_data=u["chart"],
            transaction_data=u.get("tx"),
            behavioral_data=u.get("beh")
        )

ensure_seed_golden_profiles()
