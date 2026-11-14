# -*- coding: utf-8 -*-
"""
app/logo_intelligence/five_layer_pipeline.py
============================================
Deterministic 5-Layer Logo Intelligence Pipeline for Numeros Vision (Phase 5).

Implements:
- Layer 1: Business & Category Fit (Lülfesmann & Riegel 2022, Jiang 2016, Zeng 2025,
           Luffarelli 2019, Chen 2025, Madden 2000).
- Layer 2: Read-Only Numerology Profile per Owner & up to 4 Active Partners
           (single-digit roots 1..9 only; zero 11/22/33 master exceptions).
- Layer 3: Partner Palette, Shape & Symbol Reconciliation + Charm Basis Label
           ("both systems agree" or "numerology basis only" — never alters numerology).
- Layer 4: Deterministic Vector Template Build / Upload Inspection & All 9 Hard Gates.
- Layer 5: Shukla Paksha Timing (3 verified IST dates) + Ordered Balancing Remedies
           (1. Element balancing, 2. Planet balancing, 3. Affirmation).

Every report emits FOUR SEPARATE RESULTS (never one blended score):
1. `visual_quality`
2. `brand_fit`
3. `name_intelligence` (phonetic sound profile + Chaldean compound & single-digit root)
4. `traditional_alignment`
"""

from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from app.engine.business_taxonomy import BusinessTaxonomyEngine
from app.engine.cheiro_engine import analyze_name_cheiro
from app.engine.core_matrix_engine import ELEMENT_RULES, calculate_chaldean_name
from app.engine.digit_root import calc_bhagyank, calc_driver, digit_root
from app.engine.lo_shu import analyze_lo_shu_grid
from app.logo_intelligence.rulebook_v1 import (
    EvidenceLabel,
    calculate_contrast_ratio_hex,
    classify_hex_colour_family,
    compute_free_scan_verdict,
    evaluate_contrast_gate,
    get_rulebook_v1,
    normalize_hex,
)
from app.logo_intelligence.shukla_paksha_timing import calculate_verified_shukla_paksha_window
from app.logo_intelligence.upload_inspector import inspect_svg_logo, inspect_uploaded_logo
from app.logo_intelligence.vector_templates import render_deterministic_logo_svg
from app.services.charm_deterministic_service import SWISSEPH_AVAILABLE, normalize_copy_text

try:
    import swisseph as _swe  # type: ignore
except Exception:
    _swe = None


class LogoInputError(ValueError):
    """Raised on missing/invalid user input (mapped to HTTP 400 plain message)."""

    def __init__(self, message: str, code: str = "INVALID_LOGO_INPUT") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


_TAXONOMY_ENGINE = BusinessTaxonomyEngine()

TAXONOMY_TO_RULEBOOK_CATEGORY: Dict[str, str] = {
    "footwear_apparel": "athletic_footwear",
    "sports_fitness": "sports",
    "software_ai_digital": "technology",
    "food_hospitality": "hospitality_food",
    "banking_finance_insurance": "finance",
    "education_publishing": "children_education",
    "consulting_legal_advisory": "consulting_legal",
    "beauty_luxury_fashion": "luxury_fashion_beauty",
    "healthcare_pharma_wellness": "healthcare_wellness",
    "real_estate_construction": "real_estate_infrastructure",
    "logistics_manufacturing_industrial": "real_estate_infrastructure",
    "retail_ecommerce_consumer": "retail_ecommerce",
    "media_creative_entertainment": "creative_design_media",
}

PAID_TIERS_CATALOG: List[Dict[str, Any]] = [
    {
        "tier_id": "deep_audit",
        "name": "Deep Logo Audit",
        "offer_price_inr": 510,
        "list_price_inr": 1020,
        "offer_digit_root": 6,
        "list_digit_root": 3,
        "owner_review_required": True,
        "delivery_note": "Reviewed personally by the owner before delivery.",
        "includes": [
            "Full 5-layer evaluation across all 9 hard gates",
            "Four separate pillar breakdown (visual quality, brand fit, name intelligence, traditional alignment)",
            "3 Shukla Paksha (waxing lunar fortnight) activation dates and ordered balancing steps",
        ],
    },
    {
        "tier_id": "rework",
        "name": "Existing Logo Rework",
        "offer_price_inr": 1500,
        "list_price_inr": 2400,
        "offer_digit_root": 6,
        "list_digit_root": 6,
        "owner_review_required": True,
        "delivery_note": "Reviewed personally by the owner before delivery.",
        "includes": [
            "Closed-contour vector cleanup of your existing mark",
            "Accessible colour & contrast correction reconciled across partners",
            "Master SVG + app-icon & monochrome variants",
        ],
    },
    {
        "tier_id": "new_logo",
        "name": "New Deterministic Brand Logo",
        "offer_price_inr": 3300,
        "list_price_inr": 5100,
        "offer_digit_root": 6,
        "list_digit_root": 6,
        "owner_review_required": True,
        "delivery_note": "Reviewed personally by the owner before delivery.",
        "includes": [
            "Custom 5-layer brand mark designed inside your category and partner range",
            "Horizontal, stacked, monochrome, and 64x64 app-icon pure SVG deliverables",
            "3 Shukla Paksha (waxing lunar fortnight) launch windows + brand usage sheet",
        ],
    },
    {
        "tier_id": "startup_pack",
        "name": "Startup Brand & Name Pack",
        "offer_price_inr": 6000,
        "list_price_inr": 8700,
        "offer_digit_root": 6,
        "list_digit_root": 6,
        "owner_review_required": True,
        "delivery_note": "Reviewed personally by the owner before delivery.",
        "includes": [
            "Chaldean & phonetic name alignment across up to 4 active partners",
            "Complete pure-SVG logo suite + colour & typography specification",
            "Shukla Paksha (waxing lunar fortnight) activation schedule & workspace balancing guide",
        ],
    },
]

PLANET_REMEDY_BY_ROOT: Dict[int, Dict[str, str]] = {
    1: {
        "planet_bilingual": "Surya (Sun)",
        "remedy": "Keep the East workspace clutter-free with natural morning light and honour punctual leadership commitments on Sundays.",
        "affirmation": "Our work brings clear direction, steady integrity, and honourable service to every customer.",
    },
    2: {
        "planet_bilingual": "Chandra (Moon)",
        "remedy": "Maintain calm, clean water in a glass or silver vessel in the North-East and review customer care practices on Mondays.",
        "affirmation": "Our brand listens with empathy, responds with calm clarity, and builds lasting trust.",
    },
    3: {
        "planet_bilingual": "Guru (Jupiter)",
        "remedy": "Keep learning materials and ethical charter notes orderly in the North-East and dedicate Thursday mornings to strategic planning.",
        "affirmation": "Our enterprise grows through honest counsel, sound knowledge, and fair value.",
    },
    4: {
        "planet_bilingual": "Rahu (North Lunar Node)",
        "remedy": "Maintain documented standard operating checklists, clean digital backups, and grounded South-West storage.",
        "affirmation": "Our systems stay structured, transparent, and resilient through every stage of growth.",
    },
    5: {
        "planet_bilingual": "Budh (Mercury)",
        "remedy": "Keep healthy green indoor foliage in the East or North zone and audit written client communications every Wednesday.",
        "affirmation": "Our communication is clear, adaptable, and helpful in every client exchange.",
    },
    6: {
        "planet_bilingual": "Shukra (Venus)",
        "remedy": "Keep reception and customer touchpoints neat, refined, and welcoming in the South-East, reviewing design presentation on Fridays.",
        "affirmation": "Our craft blends visual harmony, thoughtful hospitality, and dependable quality.",
    },
    7: {
        "planet_bilingual": "Ketu (South Lunar Node)",
        "remedy": "Reserve quiet weekly review time for research depth, quality inspection, and calm reflection before major releases.",
        "affirmation": "Our decisions rest on careful observation, quiet mastery, and principled focus.",
    },
    8: {
        "planet_bilingual": "Shani (Saturn)",
        "remedy": "Uphold fair team practices, disciplined timelines, and tidy West-zone storage, reviewing operational commitments on Saturdays.",
        "affirmation": "Our brand endures through patience, fair dealing, and consistent craftsmanship.",
    },
    9: {
        "planet_bilingual": "Mangal (Mars)",
        "remedy": "Channel energy into focused Tuesday execution sprints and maintain safe, well-lit South-zone equipment and workspaces.",
        "affirmation": "Our team acts with constructive courage, disciplined focus, and purposeful completion.",
    },
}

RASHI_RULER_ROOT: Tuple[int, ...] = (
    9,  # Mesha (Aries) -> Mars (9)
    6,  # Vrishabha (Taurus) -> Venus (6)
    5,  # Mithuna (Gemini) -> Mercury (5)
    2,  # Karka (Cancer) -> Moon (2)
    1,  # Simha (Leo) -> Sun (1)
    5,  # Kanya (Virgo) -> Mercury (5)
    6,  # Tula (Libra) -> Venus (6)
    9,  # Vrishchika (Scorpio) -> Mars (9)
    3,  # Dhanu (Sagittarius) -> Jupiter (3)
    8,  # Makara (Capricorn) -> Saturn (8)
    8,  # Kumbha (Aquarius) -> Saturn (8)
    3,  # Meena (Pisces) -> Jupiter (3)
)


def _clean_copy(value: Any, *, key_name: str = "") -> Any:
    preserve_keys = {
        "svg",
        "svg_markup",
        "icon_svg",
        "monochrome_svg",
        "format",
        "evidence_label",
        "basis",
        "status",
        "verdict",
        "charm_basis_label",
        "gate_id",
        "tier_id",
        "symbol_id",
        "category_id",
        "colour_family",
        "hex",
        "primary_hex",
        "accent_hex",
        "bg_hex",
        "background_hex",
        "primary_foreground_hex",
        "accent_foreground_hex",
        "extracted_text",
        "wordmark",
    }
    if key_name in preserve_keys:
        return value
    if isinstance(value, str):
        if value.startswith("#") and len(value) in (4, 7):
            return value
        if value.startswith("<svg"):
            return value
        return normalize_copy_text(value)
    if isinstance(value, list):
        return [_clean_copy(item, key_name=key_name) for item in value]
    if isinstance(value, dict):
        return {k: _clean_copy(v, key_name=k) for k, v in value.items()}
    return value


def _parse_iso_dob(dob_str: str, label: str = "Birth date") -> Tuple[int, int, int]:
    raw = (dob_str or "").strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", raw)
    if m:
        year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m_dmy = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", raw)
        if not m_dmy:
            raise LogoInputError(f"{label} must be a valid date in YYYY-MM-DD format.")
        day, month, year = int(m_dmy.group(1)), int(m_dmy.group(2)), int(m_dmy.group(3))
    try:
        dt = datetime.date(year, month, day)
    except ValueError as exc:
        raise LogoInputError(f"{label} `{raw}` is not a valid calendar date.") from exc
    if year < 1900 or dt > datetime.date(2100, 12, 31):
        raise LogoInputError(f"{label} `{raw}` is outside the supported range (1900–2100).")
    return day, month, year


def _parse_reference_date(date_str: Optional[str]) -> Optional[datetime.date]:
    if not date_str or not str(date_str).strip():
        return None
    d, m, y = _parse_iso_dob(str(date_str).strip(), label="Reference date")
    return datetime.date(y, m, d)


def analyze_phonetic_name_intelligence(business_name: str) -> Dict[str, Any]:
    """
    Deterministic phonetic sound + canonical Chaldean name intelligence:
    - Uses `calculate_chaldean_name` & `analyze_name_cheiro` (read-only).
    - `'DE WOW WAFEL'` -> compound `51`, single-digit root `6` (never 11/22/33).
    - Evaluates front vs. back vowel ratio & plosive vs. continuant consonants
      per Lowrey & Shrum (2007), Journal of Consumer Research.
    """
    clean = (business_name or "").strip()
    if not clean or not re.search(r"[A-Za-z0-9]", clean):
        raise LogoInputError("Business name must contain at least one letter or digit.")

    chaldean = calculate_chaldean_name(clean)
    cheiro = analyze_name_cheiro(clean)
    compound_num = int(chaldean["compound_number"])
    single_root = digit_root(compound_num) if compound_num > 0 else 1

    letters = [ch for ch in clean.upper() if "A" <= ch <= "Z"]
    front_vowels = sum(1 for ch in letters if ch in {"E", "I", "Y"})
    back_vowels = sum(1 for ch in letters if ch in {"A", "O", "U"})
    plosives = sum(1 for ch in letters if ch in {"P", "B", "T", "D", "K", "G"})
    sibilants_liquids = sum(1 for ch in letters if ch in {"S", "Z", "F", "V", "L", "M", "N", "R", "W"})

    if front_vowels > back_vowels:
        vowel_profile = "front_vowel_dominant"
        sound_impression = "Crisp, agile, modern, precision-leaning phonetic profile (front vowels E/I/Y lead)."
    elif back_vowels > front_vowels:
        vowel_profile = "back_vowel_dominant"
        sound_impression = "Rich, grounded, warm, enduring phonetic profile (back vowels A/O/U lead)."
    else:
        vowel_profile = "balanced_vowel_profile"
        sound_impression = "Balanced front-and-back vowel cadence suitable across broad consumer categories."

    consonant_tone = (
        "plosive_memorable_attack"
        if plosives >= sibilants_liquids and plosives > 0
        else "smooth_flowing_continuant"
    )
    word_count = len([w for w in re.split(r"\s+", clean) if w])

    rulebook = get_rulebook_v1()
    root_rule = rulebook.get_single_digit_numerology_rule(single_root)

    return {
        "exact_wordmark": clean,
        "word_count": word_count,
        "compound_number": compound_num,
        "root_number": single_root,
        "reduction_path": f"{compound_num} -> {single_root}" if compound_num >= 10 else str(single_root),
        "ruling_planet": root_rule["planet"],
        "compound_archetype": cheiro.get("compound_archetype", "Traditional Compound"),
        "compound_indication": cheiro.get("compound_characteristics", ""),
        "letter_breakdown": chaldean.get("letter_breakdown", []),
        "phonetic_profile": {
            "vowel_balance": vowel_profile,
            "front_vowel_count": front_vowels,
            "back_vowel_count": back_vowels,
            "plosive_consonant_count": plosives,
            "flowing_consonant_count": sibilants_liquids,
            "consonant_tone": consonant_tone,
            "sound_indication": sound_impression,
            "source_citation": "Lowrey & Shrum (2007), Journal of Consumer Research",
            "basis": "published research",
            "evidence_label": EvidenceLabel.PUBLISHED_RESEARCH.value,
        },
        "basis": "calculated",
        "traditional_basis": "traditional rule",
        "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
    }


def _resolve_category_id(explicit_category: Optional[str], business_name: str, activity: str) -> str:
    rulebook = get_rulebook_v1()
    valid_cats = set(rulebook.raw_data["category_norms_layer1"]["categories"].keys())
    if explicit_category and explicit_category.strip():
        cand = explicit_category.strip().lower()
        if cand in valid_cats:
            return cand
        if cand in TAXONOMY_TO_RULEBOOK_CATEGORY:
            return TAXONOMY_TO_RULEBOOK_CATEGORY[cand]
    if activity and activity.strip():
        tax = _TAXONOMY_ENGINE.classify(business_name or "", activity)
        mapped = TAXONOMY_TO_RULEBOOK_CATEGORY.get(tax.get("primary_category", ""), "")
        if mapped in valid_cats:
            return mapped
    return "UNKNOWN"


def _evaluate_charm_basis_label(
    *,
    owner_dob_tuple: Optional[Tuple[int, int, int]],
    owner_driver_root: Optional[int],
    owner_birth_time: Optional[str],
    owner_birth_lat: Optional[float],
    owner_birth_lon: Optional[float],
) -> Dict[str, Any]:
    """
    Astrology from the Charm backend ONLY adds a label:
    `"both systems agree"` or `"numerology basis only"`.
    It NEVER changes any numerology number, palette, shape, or gate decision.
    """
    if (
        not owner_dob_tuple
        or not owner_driver_root
        or not owner_birth_time
        or not str(owner_birth_time).strip()
        or not SWISSEPH_AVAILABLE
        or _swe is None
    ):
        return {
            "charm_basis_label": "numerology basis only",
            "astrology_checked": False,
            "note": "Birth time not supplied or sidereal check not requested; decisions rest on deterministic numerology basis only.",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    m = re.fullmatch(r"(\d{1,2}):(\d{2})", str(owner_birth_time).strip())
    if not m:
        return {
            "charm_basis_label": "numerology basis only",
            "astrology_checked": False,
            "note": "Birth time format not HH:MM; using numerology basis only.",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    hh, mm = int(m.group(1)), int(m.group(2))
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        return {
            "charm_basis_label": "numerology basis only",
            "astrology_checked": False,
            "note": "Birth time out of 00:00–23:59 range; using numerology basis only.",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    day, month, year = owner_dob_tuple
    utc_dt = datetime.datetime(year, month, day, hh, mm, tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30))).astimezone(datetime.timezone.utc)
    jd_ut = _swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
    _swe.set_sid_mode(_swe.SIDM_LAHIRI)
    moon_sid_lon = float(_swe.calc_ut(jd_ut, _swe.MOON, _swe.FLG_SIDEREAL)[0][0]) % 360.0
    rashi_idx = int(moon_sid_lon // 30.0) % 12
    moon_ruler_root = RASHI_RULER_ROOT[rashi_idx]

    owner_rule = get_rulebook_v1().get_single_digit_numerology_rule(owner_driver_root)
    agrees = (
        moon_ruler_root == owner_driver_root
        or moon_ruler_root in owner_rule["friendly_numbers"]
    )
    label = "both systems agree" if agrees else "numerology basis only"
    return {
        "charm_basis_label": label,
        "astrology_checked": True,
        "sidereal_ayanamsha": "Lahiri",
        "moon_rashi_index": rashi_idx + 1,
        "moon_sign_ruler_root": moon_ruler_root,
        "note": (
            "Sidereal Chandra Rashi (Moon sign) ruler aligns with the numerology profile (`both systems agree`). Astrology adds this confirmation label only and never alters numerology selections."
            if agrees
            else "Sidereal chart carries a distinct planetary emphasis (`numerology basis only`); numerology selections remain unchanged."
        ),
        "basis": "calculated",
        "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
    }


def build_partner_profiles_layer2(
    *,
    owner_name: Optional[str],
    owner_dob: Optional[str],
    partners: Optional[List[Dict[str, Any]]],
    dpdp_consent: bool,
) -> Dict[str, Any]:
    """
    Layer 2: Read-only numerology profiles for Owner + up to 4 Active Partners.
    """
    raw_partners = list(partners or [])
    active_partners = [p for p in raw_partners if isinstance(p, dict) and p.get("is_active", True) is not False]
    if len(active_partners) > 4:
        raise LogoInputError("Logo Intelligence supports up to 4 active partners in addition to the primary owner.")

    has_any_dob = bool((owner_dob and str(owner_dob).strip()) or any((p.get("dob") or "").strip() for p in active_partners))
    if has_any_dob and not dpdp_consent:
        raise LogoInputError("Explicit consent (`dpdp_consent: true`) is required before processing owner or partner birth dates.")

    rulebook = get_rulebook_v1()
    profiles: List[Dict[str, Any]] = []

    def _build_one(role: str, label_name: str, dob_val: str) -> Dict[str, Any]:
        d, m, y = _parse_iso_dob(dob_val, label=f"{label_name} birth date")
        drv = calc_driver(d)
        cond = calc_bhagyank(d, m, y)
        loshu = analyze_lo_shu_grid(d, m, y)
        drv_rule = rulebook.get_single_digit_numerology_rule(drv)
        cond_rule = rulebook.get_single_digit_numerology_rule(cond)
        sym_meta = rulebook.get_symbol_concept_for_root(drv)

        # Combine driver (primary) + conductor friendly/avoid families; enemy of either is enemy!
        fav_families = sorted({sw["colour_family"] for sw in drv_rule["favourable_swatches"] + cond_rule["favourable_swatches"]})
        avoid_families = sorted({sw["colour_family"] for sw in drv_rule["avoid_swatches"] + cond_rule["avoid_swatches"]})
        pure_fav_families = [f for f in fav_families if f not in avoid_families]

        enemy_nums = sorted(set(drv_rule["enemy_numbers"]) | set(cond_rule["enemy_numbers"]))
        friendly_nums = sorted(
            (set(drv_rule["friendly_numbers"]) | set(cond_rule["friendly_numbers"])) - set(enemy_nums)
        )
        neutral_nums = [n for n in range(1, 10) if n not in friendly_nums and n not in enemy_nums]

        return {
            "role": role,
            "name": (label_name or role.title()).strip(),
            "dob": f"{y:04d}-{m:02d}-{d:02d}",
            "driver_number": drv,
            "conductor_number": cond,
            "ruling_planet": drv_rule["planet"],
            "conductor_planet": cond_rule["planet"],
            "friendly_numbers": friendly_nums,
            "neutral_numbers": neutral_nums,
            "enemy_numbers": enemy_nums,
            "favourable_colour_families": pure_fav_families,
            "avoid_colour_families": avoid_families,
            "favourable_swatches": drv_rule["favourable_swatches"],
            "avoid_swatches": drv_rule["avoid_swatches"],
            "preferred_shape_family": sym_meta["shape_family"],
            "missing_loshu_numbers": loshu["missing_numbers"],
            "present_loshu_numbers": loshu["present_numbers"],
            "basis": "calculated",
            "rule_basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    if owner_dob and str(owner_dob).strip():
        profiles.append(_build_one("owner", owner_name or "Primary Owner", str(owner_dob).strip()))

    for idx, p in enumerate(active_partners, start=1):
        p_dob = str(p.get("dob") or "").strip()
        if not p_dob:
            continue
        p_name = str(p.get("name") or f"Active Partner {idx}").strip()
        profiles.append(_build_one(f"partner_{idx}", p_name, p_dob))

    if not profiles:
        return {
            "status": "not configured",
            "profile_count": 0,
            "profiles": [],
            "note": "No owner or active partner birth dates supplied; partner numerology profile is marked not configured.",
            "basis": "not configured",
            "evidence_label": EvidenceLabel.NOT_CONFIGURED.value,
        }

    return {
        "status": "resolved",
        "profile_count": len(profiles),
        "profiles": profiles,
        "basis": "calculated",
        "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
    }


def reconcile_layer3(
    *,
    layer1: Dict[str, Any],
    perception: Dict[str, Any],
    layer2: Dict[str, Any],
    name_intel: Dict[str, Any],
    preferred_logo_type: str = "combination_mark",
    charm_label_obj: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Layer 3 Reconciliation:
    - Common friendly colours across ALL active profiles -> Main colour.
    - Friendly to >=1 partner and neutral to all others (enemy to 0) -> Accent colours.
    - Enemy (`avoid_colour_families`) to ANY partner -> Excluded, and balanced via Layer 5 remedies.
    - Picks shape & symbol (`2, 4, 7` -> `"not configured"` -> clean wordmark/lettermark).
    """
    rulebook = get_rulebook_v1()
    all_families_data = rulebook.raw_data["colour_families"]
    all_family_ids = list(all_families_data.keys())
    allowed_cat_fams = layer1.get("allowed_colour_families") or all_family_ids

    profiles = layer2.get("profiles") or []
    name_root = int(name_intel["root_number"])
    name_rule = rulebook.get_single_digit_numerology_rule(name_root)

    # Determine ruling root for symbol lookup (owner driver if present, else business name root)
    primary_root = int(profiles[0]["driver_number"]) if profiles else name_root
    symbol_meta = rulebook.get_symbol_concept_for_root(primary_root)

    excluded_enemy_families: List[str] = []
    common_friendly_families: List[str] = []
    accent_friendly_neutral_families: List[str] = []

    if profiles:
        enemy_union: Set[str] = set()
        for prof in profiles:
            enemy_union.update(prof["avoid_colour_families"])
        excluded_enemy_families = sorted(enemy_union)

        for fam in all_family_ids:
            if fam in enemy_union or fam == "white_cream_pearl":
                continue
            fav_count = sum(1 for prof in profiles if fam in prof["favourable_colour_families"])
            if fav_count == len(profiles):
                common_friendly_families.append(fam)
            elif fav_count >= 1:
                accent_friendly_neutral_families.append(fam)
    else:
        # No partner DOBs supplied: use business name root numerology table
        name_avoid = {sw["colour_family"] for sw in name_rule["avoid_swatches"]}
        name_fav = {sw["colour_family"] for sw in name_rule["favourable_swatches"]} - name_avoid
        excluded_enemy_families = sorted(name_avoid)
        common_friendly_families = sorted(f for f in name_fav if f != "white_cream_pearl")
        accent_friendly_neutral_families = [
            f for f in allowed_cat_fams if f not in excluded_enemy_families and f not in common_friendly_families and f != "white_cream_pearl"
        ]

    # Intersect with Layer 1 category range where possible
    cat_set = set(allowed_cat_fams)
    in_range_main = [f for f in common_friendly_families if f in cat_set]
    in_range_accent = [f for f in accent_friendly_neutral_families if f in cat_set]
    safe_neutral_in_range = [
        f for f in allowed_cat_fams if f not in excluded_enemy_families and f != "white_cream_pearl"
    ]

    chosen_main_family = (
        (in_range_main[0] if in_range_main else None)
        or (common_friendly_families[0] if common_friendly_families else None)
        or (in_range_accent[0] if in_range_accent else None)
        or (accent_friendly_neutral_families[0] if accent_friendly_neutral_families else None)
        or (safe_neutral_in_range[0] if safe_neutral_in_range else "brown_earth_khaki")
    )

    accent_pool = [
        f
        for f in (in_range_accent + accent_friendly_neutral_families + in_range_main + safe_neutral_in_range)
        if f != chosen_main_family
    ]
    chosen_accent_family = accent_pool[0] if accent_pool else chosen_main_family

    def _accessible_hex_for_family(fam_id: str) -> Tuple[str, str]:
        swatches = all_families_data.get(fam_id, {}).get("canonical_swatches", {})
        for sw_name, sw in swatches.items():
            hx = normalize_hex(sw["accessible_on_light_hex"])
            if calculate_contrast_ratio_hex(hx, "#FFFDF7") >= 4.5:
                return sw_name, hx
        for sw_name, sw in swatches.items():
            return sw_name, normalize_hex(sw["accessible_on_light_hex"])
        return "Sandalwood Ink", "#523E28"

    main_swatch_name, main_hex = _accessible_hex_for_family(chosen_main_family)
    acc_swatch_name, accent_hex = _accessible_hex_for_family(chosen_accent_family)
    bg_hex = "#FFFDF7"

    # Shape reconciliation
    allowed_shapes = layer1.get("allowed_shape_families") or ["circular_curved", "balanced_hybrid", "angular_geometric"]
    promised_shape = perception["shape_guidance"]["recommended_shape_family"]
    reconciled_shape = promised_shape if promised_shape in allowed_shapes else allowed_shapes[0]

    # Logo type & symbol reconciliation (2, 4, 7 -> status == NOT_CONFIGURED -> pure wordmark/lettermark)
    req_type = (preferred_logo_type or "combination_mark").strip().lower()
    if req_type not in ("wordmark", "lettermark", "combination_mark", "emblem"):
        req_type = "combination_mark"

    if symbol_meta["status"] == "NOT_CONFIGURED":
        effective_logo_type = "lettermark" if req_type == "lettermark" else "wordmark"
        symbol_selection = {
            "root_number": primary_root,
            "status": "not configured",
            "symbol_id": None,
            "symbol_name": "not configured",
            "fallback_applied": f"Planetary symbol for root {primary_root} is not configured; using pure `{effective_logo_type}` typography without invented motifs.",
            "basis": "not configured",
            "evidence_label": EvidenceLabel.NOT_CONFIGURED.value,
        }
    else:
        effective_logo_type = req_type
        symbol_selection = {
            "root_number": primary_root,
            "status": "approved",
            "symbol_id": symbol_meta["symbol_id"],
            "symbol_name": symbol_meta["symbol_name"],
            "shape_family": symbol_meta["shape_family"],
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    return {
        "reconciled_palette": {
            "primary": {"swatch_name": main_swatch_name, "colour_family": chosen_main_family, "hex": main_hex},
            "accent": {"swatch_name": acc_swatch_name, "colour_family": chosen_accent_family, "hex": accent_hex},
            "background": {"swatch_name": "Pearl", "colour_family": "white_cream_pearl", "hex": bg_hex},
            "colour_count": len({main_hex, accent_hex, bg_hex}),
        },
        "partner_colour_matrix": {
            "common_friendly_families": common_friendly_families,
            "friendly_plus_neutral_accent_families": accent_friendly_neutral_families,
            "excluded_enemy_families": excluded_enemy_families,
            "rule_applied": "Common friendly -> main colour; friendly + neutral -> accent; enemy to any partner -> excluded and balanced via remedies.",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        },
        "reconciled_shape_family": reconciled_shape,
        "effective_logo_type": effective_logo_type,
        "symbol_selection": symbol_selection,
        "charm_astrology_alignment": charm_label_obj,
        "charm_basis_label": charm_label_obj["charm_basis_label"],
    }


def evaluate_nine_hard_gates(
    *,
    inspection: Dict[str, Any],
    expected_wordmark: Optional[str],
    layer2: Dict[str, Any],
    name_root: Optional[int],
) -> Tuple[List[Dict[str, Any]], bool, bool, List[Dict[str, Any]]]:
    """
    Evaluates all 9 Hard Gates from the Logo Intelligence Framework:
    1. `nothing_cut`
    2. `exact_text`
    3. `no_enemy_colour`
    4. `colour_count_max_3`
    5. `contrast_threshold` (>=3.0:1 symbol, >=4.5:1 small text)
    6. `monochrome_clarity`
    7. `app_icon_legibility`
    8. `max_two_fonts`
    9. `vector_integrity`
    """
    rulebook = get_rulebook_v1()
    gates: List[Dict[str, Any]] = []

    # 1. Nothing cut
    nothing_cut_ok = bool(inspection.get("nothing_cut_passed", True))
    cut_reasons = inspection.get("open_or_cut_reasons") or []
    gates.append({
        "gate_id": "nothing_cut",
        "name": "Nothing Cut (Complete Closed Outlines)",
        "passed": nothing_cut_ok,
        "measured_value": "Closed outlines" if nothing_cut_ok else "; ".join(cut_reasons),
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 2. Exact text
    extracted = (inspection.get("extracted_text") or "").strip()
    extracted_lines = [str(x).strip() for x in (inspection.get("extracted_text_lines") or []) if str(x).strip()]

    def _norm_txt(s: str) -> str:
        return re.sub(r"\s+", " ", (s or "").strip()).upper()

    if expected_wordmark and expected_wordmark.strip():
        exp_norm = _norm_txt(expected_wordmark)
        ext_norm = _norm_txt(extracted)
        ext_nospace = exp_norm.replace(" ", "") == ext_norm.replace(" ", "")
        line_hit = any(_norm_txt(ln) == exp_norm for ln in extracted_lines)
        exact_ok = bool(ext_norm == exp_norm or line_hit or (ext_nospace and float(inspection.get("text_confidence", 0.0)) >= 0.75))
        detail_txt = (
            f"Matched `{expected_wordmark.strip()}` (confidence {inspection.get('text_confidence', 0.0):.2f})"
            if exact_ok
            else f"Expected `{expected_wordmark.strip()}`, read `{extracted or 'none'}`"
        )
    else:
        exact_ok = bool(extracted and float(inspection.get("text_confidence", 0.0)) >= 0.70)
        detail_txt = (
            f"Read `{extracted}` (confidence {inspection.get('text_confidence', 0.0):.2f})"
            if exact_ok
            else "No high-confidence wordmark text detected; confirm exact text to lock evaluation"
        )
    gates.append({
        "gate_id": "exact_text",
        "name": "Exact Wordmark Text",
        "passed": exact_ok,
        "measured_value": detail_txt,
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 3. No enemy colour
    bg_hex = normalize_hex(inspection.get("background_hex") or "#FFFDF7")
    fg_palette = [
        normalize_hex(hx)
        for hx in (inspection.get("palette_sampled") or [])
        if normalize_hex(hx) != bg_hex
    ]
    if not fg_palette:
        fg_palette = [normalize_hex(inspection.get("primary_foreground_hex") or "#523E28")]

    profiles = layer2.get("profiles") or []
    enemy_hits: List[Dict[str, Any]] = []
    roots_to_check: List[Tuple[str, int]] = []
    for prof in profiles:
        roots_to_check.append((f"{prof['name']} Driver {prof['driver_number']}", int(prof["driver_number"])))
        if int(prof["conductor_number"]) != int(prof["driver_number"]):
            roots_to_check.append((f"{prof['name']} Conductor {prof['conductor_number']}", int(prof["conductor_number"])))
    if not roots_to_check and name_root in range(1, 10):
        roots_to_check.append((f"Business Name Root {name_root}", int(name_root)))

    for hx in fg_palette:
        for owner_lbl, r_num in roots_to_check:
            chk = rulebook.check_colour_against_root(hx, r_num)
            if chk["is_avoided_colour"]:
                enemy_hits.append({
                    "hex": hx,
                    "colour_family": chk["colour_family"],
                    "profile": owner_lbl,
                    "root_number": r_num,
                    "matched_avoid_names": chk["matched_avoid_names"],
                })

    # Also check name_root vs owner/partner enemy numbers
    number_conflicts: List[str] = []
    if name_root in range(1, 10):
        for prof in profiles:
            if name_root in prof["enemy_numbers"]:
                number_conflicts.append(
                    f"Name root {name_root} is in the enemy number table of {prof['name']} (Driver {prof['driver_number']} / Conductor {prof['conductor_number']})."
                )

    no_enemy_colour_ok = len(enemy_hits) == 0
    has_any_enemy_conflict = (not no_enemy_colour_ok) or (len(number_conflicts) > 0)
    gates.append({
        "gate_id": "no_enemy_colour",
        "name": "No Enemy Colour in Active Palette",
        "passed": no_enemy_colour_ok,
        "measured_value": (
            "Zero avoided colours across active numerology tables"
            if no_enemy_colour_ok
            else f"{len(enemy_hits)} avoided colour conflict(s): "
            + ", ".join(f"{h['hex']} ({h['profile']})" for h in enemy_hits[:3])
        ),
        "conflicts": enemy_hits,
        "number_conflicts": number_conflicts,
        "basis": "traditional rule",
        "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
    })

    # 4. Three colours or fewer
    colour_count = int(inspection.get("distinct_colour_count") or len(inspection.get("palette_sampled") or []))
    max_3_ok = 1 <= colour_count <= 3
    gates.append({
        "gate_id": "colour_count_max_3",
        "name": "Three Colours or Fewer",
        "passed": max_3_ok,
        "measured_value": f"{colour_count} distinct colour(s)",
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 5. Contrast threshold (>=3.0:1 symbol/large text AND >=4.5:1 small text)
    sym_contrast = float(inspection.get("min_symbol_contrast_ratio") or inspection.get("wcag_contrast_estimate") or 1.0)
    small_txt_contrast = float(inspection.get("small_text_contrast_ratio") or sym_contrast)
    primary_fg = normalize_hex(inspection.get("primary_foreground_hex") or "#523E28")
    sym_gate = evaluate_contrast_gate(primary_fg, bg_hex, usage="symbol")
    effective_sym_ratio = round(min(sym_contrast, float(sym_gate["measured_ratio"])), 2)
    contrast_ok = (effective_sym_ratio + 1e-9 >= 3.0) and (small_txt_contrast + 1e-9 >= 4.5)
    gates.append({
        "gate_id": "contrast_threshold",
        "name": "Contrast Threshold (>=3.0:1 Symbol, >=4.5:1 Small Text)",
        "passed": contrast_ok,
        "measured_value": f"Symbol/mark {effective_sym_ratio:.2f}:1 (min 3.0:1), small text {small_txt_contrast:.2f}:1 (min 4.5:1)",
        "symbol_ratio": effective_sym_ratio,
        "small_text_ratio": round(small_txt_contrast, 2),
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 6. Monochrome clarity
    mono_ok = bool(inspection.get("monochrome_clear")) and (effective_sym_ratio + 1e-9 >= 3.0)
    gates.append({
        "gate_id": "monochrome_clarity",
        "name": "Black-and-White / Single-Colour Clarity",
        "passed": mono_ok,
        "measured_value": f"Luminance ratio {effective_sym_ratio:.2f}:1 in single-tone conversion",
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 7. App-icon legibility
    dims = inspection.get("dimensions") or {"width": 0, "height": 0}
    icon_ok = bool(inspection.get("app_icon_legible")) and int(dims.get("width", 0)) >= 64 and int(dims.get("height", 0)) >= 48
    gates.append({
        "gate_id": "app_icon_legibility",
        "name": "Legible at App-Icon Size (64x64 / 32x32)",
        "passed": icon_ok,
        "measured_value": f"{dims.get('width', 0)}x{dims.get('height', 0)}px ({'legible at 64x64' if icon_ok else 'insufficient small-size contrast or resolution < 64px'})",
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 8. Two typefaces or fewer
    font_cnt = int(inspection.get("font_count") or 0)
    fonts_ok = font_cnt <= 2
    gates.append({
        "gate_id": "max_two_fonts",
        "name": "Two Typefaces or Fewer",
        "passed": fonts_ok,
        "measured_value": f"{font_cnt} typeface family/families" + (
            f" ({', '.join(inspection.get('font_families') or [])})" if inspection.get("font_families") else ""
        ),
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    # 9. Clean pure SVG vector integrity
    vec_ok = bool(inspection.get("is_vector")) and not bool(inspection.get("has_embedded_raster")) and not bool(inspection.get("has_unsafe_script"))
    vec_reason = "Pure closed-path vector SVG"
    if not vec_ok:
        if inspection.get("has_unsafe_script"):
            vec_reason = "Contains disallowed inline <script> or event handler"
        elif inspection.get("format") == "SVG" and inspection.get("has_embedded_raster"):
            vec_reason = "SVG wraps an embedded raster <image> instead of pure vector paths"
        else:
            vec_reason = f"Uploaded `{inspection.get('format')}` is raster/non-SVG; pure SVG master required for signage & print"
    gates.append({
        "gate_id": "vector_integrity",
        "name": "Clean Pure SVG Vector",
        "passed": vec_ok,
        "measured_value": vec_reason,
        "basis": "calculated",
        "evidence_label": EvidenceLabel.MEASURED.value,
    })

    all_passed = all(g["passed"] for g in gates)
    return gates, all_passed, has_any_enemy_conflict, enemy_hits


def build_layer5_activation(
    *,
    reference_date: Optional[datetime.date],
    ruling_root: int,
    layer2: Dict[str, Any],
    excluded_enemy_families: List[str],
    enemy_hits: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Layer 5 Activation & Balancing:
    1. Three dates strictly inside Shukla Paksha (verified IST astronomy & panchang).
    2. Ordered remedies:
       Step 1: Element balancing
       Step 2: Planet balancing
       Step 3: Affirmation
    """
    timing = calculate_verified_shukla_paksha_window(
        reference_date=reference_date,
        ruling_root=ruling_root,
    )

    # Determine missing elements from Owner Lo Shu grid (if available)
    profiles = layer2.get("profiles") or []
    missing_elements: List[Dict[str, str]] = []
    if profiles:
        missing_nums = set(profiles[0].get("missing_loshu_numbers") or [])
        for elem_name, meta in ELEMENT_RULES.items():
            if all(n in missing_nums for n in meta["numbers"]):
                missing_elements.append({
                    "element": elem_name,
                    "remedy": meta["deficient_remedy"],
                    "basis": "traditional rule",
                })
    if not missing_elements:
        root_elem = get_rulebook_v1().get_single_digit_numerology_rule(ruling_root)["element"]
        elem_meta = ELEMENT_RULES.get(root_elem, ELEMENT_RULES["Earth"])
        missing_elements.append({
            "element": root_elem,
            "remedy": elem_meta["deficient_remedy"],
            "basis": "traditional rule",
        })

    planet_entry = PLANET_REMEDY_BY_ROOT.get(ruling_root, PLANET_REMEDY_BY_ROOT[1])
    enemy_balance_note = ""
    if excluded_enemy_families or enemy_hits:
        fam_list = sorted(set(excluded_enemy_families) | {h["colour_family"] for h in enemy_hits})
        enemy_balance_note = (
            f" Excluded or conflicting colour family ({', '.join(fam_list[:3])}) is kept out of the primary brand mark "
            f"and balanced through workspace element grounding rather than forced into the logo."
        )

    ordered_remedies = [
        {
            "step": 1,
            "category": "element_balancing",
            "title": "1. Element Balancing",
            "guidance": f"{missing_elements[0]['element']} balance: {missing_elements[0]['remedy']}{enemy_balance_note}",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        },
        {
            "step": 2,
            "category": "planet_remedies",
            "title": f"2. Planetary Rhythm ({planet_entry['planet_bilingual']})",
            "guidance": planet_entry["remedy"],
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        },
        {
            "step": 3,
            "category": "affirmation",
            "title": "3. Brand Stewardship Affirmation",
            "guidance": planet_entry["affirmation"],
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        },
    ]

    return {
        "timing": timing,
        "three_shukla_paksha_dates": timing["three_shukla_paksha_dates"],
        "ordered_remedies": ordered_remedies,
        "basis": "calculated",
        "traditional_basis": "traditional rule",
    }


def run_five_layer_logo_evaluation(payload: Dict[str, Any], *, uploaded_bytes: Optional[bytes] = None, uploaded_filename: Optional[str] = None, uploaded_mime: Optional[str] = None) -> Dict[str, Any]:
    """
    Full 5-Layer Logo Intelligence evaluation for both:
    - `intake_mode="new_logo"` (or default when no upload is supplied)
    - `intake_mode="audit_existing"` (when SVG/PNG/JPEG/PDF upload is supplied)
    """
    if not isinstance(payload, dict):
        raise LogoInputError("Request payload must be a JSON object.")

    intake_mode = str(payload.get("intake_mode") or ("audit_existing" if (uploaded_bytes or payload.get("svg_content") or payload.get("image_base64") or payload.get("file_base64")) else "new_logo")).strip().lower()
    business_name = str(payload.get("business_name") or payload.get("confirmed_text") or "").strip()

    has_upload = bool(
        uploaded_bytes is not None
        or (payload.get("svg_content") and str(payload.get("svg_content")).strip())
        or (payload.get("image_base64") and str(payload.get("image_base64")).strip())
        or (payload.get("file_base64") and str(payload.get("file_base64")).strip())
    )

    if not business_name and not has_upload:
        raise LogoInputError("Provide `business_name` (and/or upload a PNG, JPEG, PDF, or SVG logo file) to run Logo Intelligence.")

    # Parse 17 intake fields cleanly (never inventing defaults for missing business/birth facts)
    tagline = str(payload.get("tagline") or "").strip() or None
    business_activity = str(payload.get("business_activity") or "").strip()
    product_function = str(payload.get("product_function") or "").strip()
    customer_outcome = str(payload.get("customer_outcome") or "").strip()
    target_audience = str(payload.get("target_audience") or "").strip()
    market_region = str(payload.get("market_region") or "INDIA").strip().upper()
    if market_region not in ("INDIA", "INTERNATIONAL"):
        raise LogoInputError("`market_region` must be `INDIA` or `INTERNATIONAL`.")
    price_position = str(payload.get("price_position") or "mid").strip().lower()
    if price_position not in ("value", "mid", "premium"):
        price_position = "mid"
    brand_stage = str(payload.get("brand_stage") or "startup").strip().lower()
    raw_personality = payload.get("brand_personality") or []
    if isinstance(raw_personality, str):
        personality_words = [w.strip() for w in raw_personality.split(",") if w.strip()]
    elif isinstance(raw_personality, list):
        personality_words = [str(w).strip() for w in raw_personality if str(w).strip()]
    else:
        personality_words = []

    preferred_logo_type = str(payload.get("preferred_logo_type") or "combination_mark").strip().lower()
    lockup_variant = str(payload.get("lockup_variant") or payload.get("variant") or "horizontal_lockup").strip().lower()
    primary_touchpoint = str(payload.get("primary_touchpoint") or "app_web").strip().lower()
    dpdp_consent = bool(payload.get("dpdp_consent", False))

    # Inspect upload first if provided so OCR wordmark can inform name intelligence if `business_name` was omitted
    inspection: Optional[Dict[str, Any]] = None
    if has_upload:
        try:
            inspection = inspect_uploaded_logo(
                svg_content=payload.get("svg_content"),
                file_bytes=uploaded_bytes,
                image_base64=payload.get("image_base64") or payload.get("file_base64"),
                filename=uploaded_filename or payload.get("filename"),
                mime_type=uploaded_mime or payload.get("mime_type"),
                confirmed_text=payload.get("confirmed_text"),
                confirmed_primary_color=payload.get("confirmed_primary_color"),
                confirmed_accent_color=payload.get("confirmed_accent_color"),
                confirmed_bg_color=payload.get("confirmed_bg_color"),
            )
        except ValueError as exc:
            raise LogoInputError(str(exc)) from exc

    effective_name_for_calc = business_name or (inspection.get("extracted_text", "").strip() if inspection else "")
    if effective_name_for_calc and re.search(r"[A-Za-z0-9]", effective_name_for_calc):
        name_intel = analyze_phonetic_name_intelligence(effective_name_for_calc)
    else:
        name_intel = {
            "exact_wordmark": "",
            "status": "not configured",
            "compound_number": None,
            "root_number": 1,
            "note": "Exact business name was not supplied or readable from upload; enter or confirm the wordmark to calculate Chaldean and sound intelligence.",
            "basis": "not configured",
            "evidence_label": EvidenceLabel.NOT_CONFIGURED.value,
        }

    # Layer 1: Business & Category Fit
    rulebook = get_rulebook_v1()
    resolved_cat = _resolve_category_id(
        payload.get("business_category") or payload.get("category"),
        effective_name_for_calc,
        " ".join(x for x in (business_activity, product_function, customer_outcome) if x),
    )
    layer1 = rulebook.get_layer1_category_profile(resolved_cat, region=market_region)
    perception = rulebook.derive_shape_and_lightness_guidance(personality_words, price_position=price_position)

    # Layer 2: Read-Only Owner + Up to 4 Active Partners
    owner_dob_raw = payload.get("owner_dob") or payload.get("founder_dob")
    layer2 = build_partner_profiles_layer2(
        owner_name=payload.get("owner_name") or payload.get("founder_name"),
        owner_dob=owner_dob_raw,
        partners=payload.get("partners"),
        dpdp_consent=dpdp_consent,
    )

    owner_dob_tuple: Optional[Tuple[int, int, int]] = None
    owner_driver: Optional[int] = None
    if layer2["profiles"]:
        owner_dob_tuple = _parse_iso_dob(layer2["profiles"][0]["dob"])
        owner_driver = int(layer2["profiles"][0]["driver_number"])

    charm_label_obj = _evaluate_charm_basis_label(
        owner_dob_tuple=owner_dob_tuple,
        owner_driver_root=owner_driver,
        owner_birth_time=payload.get("owner_birth_time"),
        owner_birth_lat=payload.get("owner_birth_lat"),
        owner_birth_lon=payload.get("owner_birth_lon"),
    )

    # Layer 3: Reconciliation
    layer3 = reconcile_layer3(
        layer1=layer1,
        perception=perception,
        layer2=layer2,
        name_intel=name_intel,
        preferred_logo_type=preferred_logo_type,
        charm_label_obj=charm_label_obj,
    )

    # Layer 4: Deterministic Vector Build (when new_logo) + 9 Hard Gates
    generated_assets: Optional[Dict[str, str]] = None
    if inspection is None:
        if not business_name:
            raise LogoInputError("`business_name` is required to build a new logo preview.")
        rec_pal = layer3["reconciled_palette"]
        p_hex = normalize_hex(payload.get("primary_color") or rec_pal["primary"]["hex"])
        a_hex = normalize_hex(payload.get("accent_color") or rec_pal["accent"]["hex"])
        b_hex = normalize_hex(payload.get("bg_color") or rec_pal["background"]["hex"])
        sym_id = payload.get("symbol_concept") or layer3["symbol_selection"].get("symbol_id")

        master_svg = render_deterministic_logo_svg(
            exact_wordmark=business_name,
            symbol_id=sym_id,
            logo_type=layer3["effective_logo_type"],
            variant=lockup_variant,
            primary_hex=p_hex,
            accent_hex=a_hex,
            bg_hex=b_hex,
            tagline=tagline,
        )
        icon_svg = render_deterministic_logo_svg(
            exact_wordmark=business_name,
            symbol_id=sym_id,
            logo_type=layer3["effective_logo_type"],
            variant="icon",
            primary_hex=p_hex,
            accent_hex=a_hex,
            bg_hex=b_hex,
        )
        mono_svg = render_deterministic_logo_svg(
            exact_wordmark=business_name,
            symbol_id=sym_id,
            logo_type=layer3["effective_logo_type"],
            variant=lockup_variant,
            primary_hex="#523E28",
            accent_hex="#523E28",
            bg_hex="#FFFDF7",
            tagline=tagline,
        )
        generated_assets = {
            "svg": master_svg,
            "icon_svg": icon_svg,
            "monochrome_svg": mono_svg,
        }
        inspection = inspect_svg_logo(master_svg)

    hard_gates, all_hard_passed, has_enemy_conflict, enemy_hits = evaluate_nine_hard_gates(
        inspection=inspection,
        expected_wordmark=business_name or None,
        layer2=layer2,
        name_root=name_intel.get("root_number") if name_intel.get("compound_number") is not None else None,
    )

    # Layer 5: Shukla Paksha Timing + Ordered Remedies
    ruling_root = int(owner_driver or name_intel.get("root_number") or 1)
    ref_date = _parse_reference_date(payload.get("reference_date"))
    layer5 = build_layer5_activation(
        reference_date=ref_date,
        ruling_root=ruling_root,
        layer2=layer2,
        excluded_enemy_families=layer3["partner_colour_matrix"]["excluded_enemy_families"],
        enemy_hits=enemy_hits,
    )

    # Four Separate Results (NEVER one blended score)
    passed_gate_count = sum(1 for g in hard_gates if g["passed"])
    failed_gates = [g for g in hard_gates if not g["passed"]]

    # Check category fit of active primary foreground colour
    active_primary_fam = classify_hex_colour_family(inspection["primary_foreground_hex"])["colour_family"]
    cat_allowed = layer1.get("allowed_colour_families") or []
    cat_fit_status = (
        "not configured"
        if layer1["status"] != "RESOLVED"
        else ("aligned" if active_primary_fam in cat_allowed else "outside_category_norm")
    )

    four_results = {
        "visual_quality": {
            "pillar": "Visual Quality",
            "status": "aligned" if all(g["passed"] for g in hard_gates if g["gate_id"] != "no_enemy_colour") else "needs_attention",
            "gates_passed": f"{sum(1 for g in hard_gates if g['gate_id'] != 'no_enemy_colour' and g['passed'])}/8 technical gates",
            "contrast_ratio": f"{inspection['wcag_contrast_estimate']:.2f}:1",
            "is_pure_vector": inspection["is_vector"],
            "nothing_cut": inspection["nothing_cut_passed"],
            "app_icon_legible": inspection["app_icon_legible"],
            "font_count": inspection["font_count"],
            "basis": "calculated",
            "evidence_label": EvidenceLabel.MEASURED.value,
        },
        "brand_fit": {
            "pillar": "Brand & Category Fit",
            "status": cat_fit_status,
            "category_id": layer1["category_id"],
            "active_primary_colour_family": active_primary_fam,
            "allowed_category_colour_families": cat_allowed,
            "recommended_shape_family": perception["shape_guidance"]["recommended_shape_family"],
            "recommended_lightness": perception["lightness_guidance"]["recommended_lightness"],
            "market_region": market_region,
            "startup_descriptiveness_note": (
                "Descriptive visual cues improve initial comprehension for unfamiliar startup brands (Luffarelli et al., 2019)."
                if brand_stage == "startup"
                else "Established brands may use cleaner simplified forms for competence cues (Chen et al., 2025)."
            ),
            "basis": "published research" if layer1["status"] == "RESOLVED" else "not configured",
            "evidence_label": layer1["evidence_label"],
        },
        "name_intelligence": {
            "pillar": "Name Intelligence (Sound + Chaldean Number)",
            "status": "calculated" if name_intel.get("compound_number") is not None else "not configured",
            "wordmark": name_intel.get("exact_wordmark", ""),
            "compound_number": name_intel.get("compound_number"),
            "root_number": name_intel.get("root_number") if name_intel.get("compound_number") is not None else None,
            "ruling_planet": name_intel.get("ruling_planet"),
            "compound_archetype": name_intel.get("compound_archetype"),
            "phonetic_profile": name_intel.get("phonetic_profile"),
            "basis": "calculated" if name_intel.get("compound_number") is not None else "not configured",
            "evidence_label": name_intel["evidence_label"],
        },
        "traditional_alignment": {
            "pillar": "Traditional Numerology & Timing Alignment",
            "status": "aligned" if not has_enemy_conflict else "conflict_detected",
            "partner_profiles_evaluated": layer2["profile_count"],
            "reconciled_palette": layer3["reconciled_palette"],
            "excluded_enemy_families": layer3["partner_colour_matrix"]["excluded_enemy_families"],
            "symbol_selection": layer3["symbol_selection"],
            "charm_basis_label": layer3["charm_basis_label"],
            "shukla_paksha_window": f"{layer5['timing']['shukla_paksha_start_date']} to {layer5['timing']['shukla_paksha_end_date']}",
            "basis": "traditional rule",
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        },
    }

    # Free Scan Verdict + Up to 3 Named Gaps
    verdict_obj = compute_free_scan_verdict(all_hard_passed, has_enemy_conflict)
    named_gaps: List[str] = []
    for fg in failed_gates:
        named_gaps.append(f"{fg['name']}: {fg['measured_value']}")
        if len(named_gaps) >= 3:
            break
    if len(named_gaps) < 3 and cat_fit_status == "outside_category_norm":
        named_gaps.append(
            f"Category Fit: `{active_primary_fam}` sits outside `{layer1['category_id']}` norms ({', '.join(cat_allowed[:3])})."
        )

    intake_summary = {
        "q01_business_name": business_name or "not configured",
        "q02_tagline": tagline or "not configured",
        "q03_intake_mode": intake_mode,
        "q04_business_category": layer1["category_id"],
        "q05_business_activity": business_activity or "not configured",
        "q06_product_function": product_function or "not configured",
        "q07_customer_outcome": customer_outcome or "not configured",
        "q08_target_audience": target_audience or "not configured",
        "q09_market_region": market_region,
        "q10_price_position": price_position,
        "q11_brand_stage": brand_stage,
        "q12_brand_personality": personality_words or ["not configured"],
        "q13_preferred_logo_type": preferred_logo_type,
        "q14_lockup_variant": lockup_variant,
        "q15_primary_touchpoint": primary_touchpoint,
        "q16_active_partners_count": max(0, layer2["profile_count"] - 1),
        "q17_dpdp_consent": dpdp_consent,
    }

    result: Dict[str, Any] = {
        "ok": True,
        "intake_mode": intake_mode,
        "intake_summary": intake_summary,
        "free_scan": {
            "verdict": verdict_obj["verdict"],
            "hard_gates_passed_count": passed_gate_count,
            "hard_gates_total": len(hard_gates),
            "named_gaps": named_gaps[:3],
            "basis": "calculated",
            "evidence_label": verdict_obj["evidence_label"],
        },
        "four_results": four_results,
        "hard_gates": hard_gates,
        "upload_reading": {
            "format": inspection["format"],
            "extracted_text": inspection["extracted_text"],
            "text_confidence": inspection["text_confidence"],
            "primary_foreground_hex": inspection["primary_foreground_hex"],
            "accent_foreground_hex": inspection["accent_foreground_hex"],
            "background_hex": inspection["background_hex"],
            "palette_sampled": inspection["palette_sampled"],
            "dominant_colors": inspection["dominant_colors"],
            "colour_confidence": inspection["colour_confidence"],
            "user_corrected": inspection["user_corrected"],
            "can_user_override": True,
            "override_fields": [
                "confirmed_text",
                "confirmed_primary_color",
                "confirmed_accent_color",
                "confirmed_bg_color",
            ],
        },
        "layers": {
            "layer1_business_fit": {**layer1, "perception_rules": perception},
            "layer2_partner_profiles": layer2,
            "layer3_reconciliation": layer3,
            "layer4_build_and_gates": {
                "inspection": inspection,
                "hard_gates": hard_gates,
                "all_hard_gates_passed": all_hard_passed,
            },
            "layer5_activation": layer5,
        },
        "paid_tiers": PAID_TIERS_CATALOG,
        "owner_review_policy": "Every paid output is reviewed by the owner before delivery.",
    }
    if generated_assets is not None:
        result["generated_assets"] = generated_assets
        result["svg"] = generated_assets["svg"]

    return _clean_copy(result)


def run_logo_preview_endpoint(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic `/api/v1/logo/preview` handler:
    - Validates `business_name` (HTTP 400 when missing/empty — zero invented fallback names).
    - Renders honest pure-SVG without silent colour substitution (`#C9A227` on `#FFFDF7`
      stays `#C9A227`, measures `2.38:1`, and fails `contrast_threshold`!).
    """
    if not isinstance(payload, dict):
        raise LogoInputError("JSON body must be an object.")
    bname = str(payload.get("business_name") or "").strip()
    if not bname:
        raise LogoInputError("`business_name` is required to generate a logo preview.")

    try:
        p_hex = normalize_hex(str(payload.get("primary_color") or "#523E28"))
        a_hex = normalize_hex(str(payload.get("accent_color") or "#16835B"))
        b_hex = normalize_hex(str(payload.get("bg_color") or "#FFFDF7"))
    except ValueError as exc:
        raise LogoInputError(str(exc)) from exc

    eval_payload = dict(payload)
    eval_payload["intake_mode"] = "new_logo"
    eval_payload["primary_color"] = p_hex
    eval_payload["accent_color"] = a_hex
    eval_payload["bg_color"] = b_hex

    full_eval = run_five_layer_logo_evaluation(eval_payload)
    insp = full_eval["layers"]["layer4_build_and_gates"]["inspection"]
    return {
        "ok": True,
        "business_name": bname,
        "variant": str(payload.get("variant") or "horizontal_lockup"),
        "svg": full_eval["svg"],
        "generated_assets": full_eval["generated_assets"],
        "contrast_ratio": insp["wcag_contrast_estimate"],
        "contrast_passed": any(
            g["gate_id"] == "contrast_threshold" and g["passed"] for g in full_eval["hard_gates"]
        ),
        "all_hard_gates_passed": full_eval["layers"]["layer4_build_and_gates"]["all_hard_gates_passed"],
        "free_scan": full_eval["free_scan"],
        "four_results": full_eval["four_results"],
        "hard_gates": full_eval["hard_gates"],
        "name_numerology": full_eval["four_results"]["name_intelligence"],
        "shukla_paksha": full_eval["layers"]["layer5_activation"]["timing"],
        "paid_tiers": full_eval["paid_tiers"],
    }


def run_analyze_existing_endpoint(
    payload: Dict[str, Any],
    *,
    uploaded_bytes: Optional[bytes] = None,
    uploaded_filename: Optional[str] = None,
    uploaded_mime: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Deterministic `/api/v1/logo/analyze-existing` handler supporting SVG, PNG, JPEG, and PDF.
    Populates both `measurable_findings` (`palette_sampled` + `dominant_colors`) AND full
    5-layer `hard_gates`, `four_results`, and `free_scan`!
    """
    eval_payload = dict(payload or {})
    eval_payload["intake_mode"] = "audit_existing"
    full_eval = run_five_layer_logo_evaluation(
        eval_payload,
        uploaded_bytes=uploaded_bytes,
        uploaded_filename=uploaded_filename,
        uploaded_mime=uploaded_mime,
    )
    insp = full_eval["layers"]["layer4_build_and_gates"]["inspection"]
    return {
        "ok": True,
        "measurable_findings": insp,
        "upload_reading": full_eval["upload_reading"],
        "free_scan": full_eval["free_scan"],
        "four_results": full_eval["four_results"],
        "hard_gates": full_eval["hard_gates"],
        "layers": full_eval["layers"],
        "paid_tiers": full_eval["paid_tiers"],
        "owner_review_policy": full_eval["owner_review_policy"],
    }
