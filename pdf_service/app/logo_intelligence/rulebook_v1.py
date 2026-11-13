"""
NUMEROS VISION — Logo Intelligence Rule Set v1 (`rulebook_v1.py`)
=================================================================
Single server-side rule loader and deterministic evaluator for Logo Studio v1.

Guarantees:
1. Read-only binding to `app.engine.number_characteristics_registry.NUMBER_REGISTRY`
   for single-digit roots `1..9` (zero modification to existing engines).
2. Enforces Locked Decision D6: Client logo palettes follow the client's own
   numerology tables (no blanket navy or black ban on client logos).
3. Enforces 1-to-9 Symbol Concept Table: roots `1, 3, 5, 6, 8, 9` return their
   approved vector concepts; roots `2, 4, 7` strictly return `"Not configured"`
   (`status="NOT_CONFIGURED"`, `symbol_id=None`, zero fallback guessing).
4. Enforces `APPROVED`-only business archetype governance: draft proposals
   (`SPORTS_ARCHETYPE_SATURN_8`, `SPORTS_ARCHETYPE_KETU_7`,
   `BUSINESS_ARCHETYPE_SATURN_001`, `BUSINESS_ARCHETYPE_RAHU_001`) are excluded
   from active scoring and surface as `NOT_CONFIGURED`.
5. Every rule output carries an explicit `evidence_label` in
   `{"MEASURED", "PUBLISHED_RESEARCH", "TRADITIONAL_RULE", "NOT_CONFIGURED"}`.
"""

from __future__ import annotations

import colorsys
import copy
import enum
import json
import math
import pathlib
from typing import Any, Dict, List, Optional, Tuple

from app.engine.number_characteristics_registry import NUMBER_REGISTRY


class EvidenceLabel(str, enum.Enum):
    MEASURED = "MEASURED"
    PUBLISHED_RESEARCH = "PUBLISHED_RESEARCH"
    TRADITIONAL_RULE = "TRADITIONAL_RULE"
    NOT_CONFIGURED = "NOT_CONFIGURED"


VALID_EVIDENCE_LABELS = frozenset(item.value for item in EvidenceLabel)
SINGLE_DIGIT_ROOTS = tuple(range(1, 10))
VALID_REGIONS = frozenset({"INDIA", "INTERNATIONAL"})


def assert_valid_evidence_label(label: str) -> str:
    if label not in VALID_EVIDENCE_LABELS:
        raise ValueError(
            f"Invalid evidence_label {label!r}; expected one of {sorted(VALID_EVIDENCE_LABELS)}."
        )
    return label


def normalize_hex(hex_code: str) -> str:
    if not isinstance(hex_code, str):
        raise ValueError(f"HEX colour must be a string, got {type(hex_code).__name__}")
    raw = hex_code.strip().lstrip("#")
    if len(raw) == 3 and all(c in "0123456789abcdefABCDEF" for c in raw):
        raw = "".join(c * 2 for c in raw)
    if len(raw) != 6 or not all(c in "0123456789abcdefABCDEF" for c in raw):
        raise ValueError(f"Invalid HEX colour code: {hex_code!r}")
    return f"#{raw.upper()}"


def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    norm = normalize_hex(hex_code)[1:]
    return int(norm[0:2], 16), int(norm[2:4], 16), int(norm[4:6], 16)


def calculate_relative_luminance(rgb: Tuple[int, int, int]) -> float:
    """WCAG 2.1 relative luminance for 8-bit sRGB tuple."""
    lin: List[float] = []
    for channel in rgb:
        s = channel / 255.0
        if s <= 0.03928:
            lin.append(s / 12.92)
        else:
            lin.append(((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def calculate_contrast_ratio_hex(fg_hex: str, bg_hex: str) -> float:
    """Deterministic WCAG 2.1 contrast ratio (1.0 to 21.0) between two HEX colours."""
    l1 = calculate_relative_luminance(hex_to_rgb(fg_hex))
    l2 = calculate_relative_luminance(hex_to_rgb(bg_hex))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate_contrast_gate(
    fg_hex: str,
    bg_hex: str,
    usage: str = "small_text",
) -> Dict[str, Any]:
    """
    Evaluates contrast ratio against Rule Set v1 hard thresholds:
    - `symbol` or `large_text`: minimum `3.0:1`
    - `small_text`: minimum `4.5:1`
    Specifically confirms `#C9A227` on `#523E28` (`4.18:1`) passes for symbol/large_text
    only and fails for small_text, while `#C9A227` on `#FFFDF7` (`2.38:1`) fails all three.
    """
    if usage not in ("symbol", "large_text", "small_text"):
        raise ValueError(f"Unsupported contrast usage {usage!r}; use 'symbol', 'large_text', or 'small_text'.")

    fg_norm = normalize_hex(fg_hex)
    bg_norm = normalize_hex(bg_hex)
    raw_ratio = calculate_contrast_ratio_hex(fg_norm, bg_norm)
    measured_ratio = round(raw_ratio, 2)
    required_ratio = 3.0 if usage in ("symbol", "large_text") else 4.5
    passed = raw_ratio + 1e-9 >= required_ratio

    allowed_usages: List[str] = []
    if raw_ratio + 1e-9 >= 3.0:
        allowed_usages.extend(["symbol", "large_text"])
    if raw_ratio + 1e-9 >= 4.5:
        allowed_usages.append("small_text")

    return {
        "foreground_hex": fg_norm,
        "background_hex": bg_norm,
        "usage": usage,
        "measured_ratio": measured_ratio,
        "required_ratio": required_ratio,
        "passed": passed,
        "allowed_usages": allowed_usages,
        "symbol_and_large_text_only": ("symbol" in allowed_usages and "small_text" not in allowed_usages),
        "evidence_label": EvidenceLabel.MEASURED.value,
    }


def compute_free_scan_verdict(hard_gates_all_passed: bool, has_enemy_conflict: bool) -> Dict[str, str]:
    """
    Confirmed three-state Free Scan verdict rule:
    - `Aligned`: all hard gates pass AND zero enemy colour/number conflicts.
    - `Partly aligned`: either a hard gate fails OR a conflict exists, not both.
    - `Not aligned`: both a hard gate failure AND an enemy conflict exist.
    """
    hard_failed = not bool(hard_gates_all_passed)
    conflict = bool(has_enemy_conflict)
    if not hard_failed and not conflict:
        verdict = "Aligned"
    elif hard_failed and conflict:
        verdict = "Not aligned"
    else:
        verdict = "Partly aligned"
    return {
        "verdict": verdict,
        "evidence_label": EvidenceLabel.MEASURED.value,
    }


def _resolve_rules_json_path() -> pathlib.Path:
    """Locates `data/logo_rules_v1.json` across both repo root and `pdf_service/` Docker root."""
    here = pathlib.Path(__file__).resolve()
    candidates = [
        here.parents[2] / "data" / "logo_rules_v1.json",
        here.parents[1] / "data" / "logo_rules_v1.json",
        pathlib.Path.cwd() / "data" / "logo_rules_v1.json",
    ]
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(
        f"logo_rules_v1.json not found in any expected data path: {[str(c) for c in candidates]}"
    )


def classify_hex_colour_family(hex_code: str, rules_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Deterministically classifies any HEX colour into one of the 12 Rule Set v1 colour families
    plus lightness/saturation metrics (`evidence_label="MEASURED"`).
    """
    norm = normalize_hex(hex_code)
    r, g, b = hex_to_rgb(norm)
    lum = calculate_relative_luminance((r, g, b))
    h_unit, l_hls, s_hls = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    _, s_hsv, v_hsv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
    hue_deg = h_unit * 360.0

    # 1. Exact canonical swatch hit first (if rules_data provided or loaded)
    catalog = (rules_data or get_rulebook_v1().raw_data).get("colour_families", {})
    for fam_id, fam_info in catalog.items():
        for swatch_name, sw in fam_info.get("canonical_swatches", {}).items():
            if normalize_hex(sw["canonical_hex"]) == norm:
                return {
                    "hex": norm,
                    "colour_family": fam_id,
                    "matched_swatch_name": swatch_name,
                    "relative_luminance": round(lum, 4),
                    "hue_deg": round(hue_deg, 1),
                    "saturation_hsv": round(s_hsv, 3),
                    "value_hsv": round(v_hsv, 3),
                    "is_dark": lum < 0.18,
                    "evidence_label": EvidenceLabel.MEASURED.value,
                }

    # 2. Achromatic / near-achromatic buckets
    if s_hsv < 0.14 or (v_hsv < 0.18 and s_hsv < 0.30):
        if v_hsv <= 0.24:
            family = "black_charcoal"
        elif l_hls >= 0.90:
            family = "white_cream_pearl"
        else:
            family = "grey_silver"
    # 3. Very light warm ivory / cream / pearl
    elif l_hls >= 0.92 and 25.0 <= hue_deg <= 75.0 and s_hls <= 0.65:
        family = "white_cream_pearl"
    # 4. Chromatic buckets by hue, value, and saturation
    elif hue_deg < 14.0 or hue_deg >= 345.0:
        if l_hls >= 0.76 and s_hsv < 0.55:
            family = "pink_rose"
        else:
            family = "red_crimson_coral"
    elif 14.0 <= hue_deg < 41.0:
        if v_hsv < 0.45 and s_hsv < 0.65:
            family = "brown_earth_khaki"
        else:
            family = "orange_amber_copper"
    elif 41.0 <= hue_deg < 68.0:
        if v_hsv < 0.52 and s_hsv < 0.55:
            family = "brown_earth_khaki"
        else:
            family = "gold_yellow"
    elif 68.0 <= hue_deg < 172.0:
        family = "green_emerald_mint"
    elif 172.0 <= hue_deg < 252.0:
        if v_hsv <= 0.56 and hue_deg >= 200.0:
            family = "navy_dark_blue"
        else:
            family = "blue_sky_electric"
    elif 252.0 <= hue_deg < 305.0:
        family = "purple_lavender"
    else:  # 305..345
        family = "pink_rose"

    # Find nearest swatch inside that family for transparent reporting
    nearest_name = None
    nearest_dist = float("inf")
    fam_swatches = catalog.get(family, {}).get("canonical_swatches", {})
    for sw_name, sw in fam_swatches.items():
        sr, sg, sb = hex_to_rgb(sw["canonical_hex"])
        dist = math.sqrt((r - sr) ** 2 + (g - sg) ** 2 + (b - sb) ** 2)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest_name = sw_name

    return {
        "hex": norm,
        "colour_family": family,
        "matched_swatch_name": nearest_name,
        "relative_luminance": round(lum, 4),
        "hue_deg": round(hue_deg, 1),
        "saturation_hsv": round(s_hsv, 3),
        "value_hsv": round(v_hsv, 3),
        "is_dark": lum < 0.18,
        "evidence_label": EvidenceLabel.MEASURED.value,
    }


class LogoRulebookV1:
    """Immutable-view facade over `data/logo_rules_v1.json` and read-only `NUMBER_REGISTRY`."""

    def __init__(self, json_path: Optional[pathlib.Path] = None) -> None:
        self.json_path = json_path or _resolve_rules_json_path()
        with open(self.json_path, "r", encoding="utf-8") as fh:
            self._data: Dict[str, Any] = json.load(fh)
        self._swatch_lookup: Dict[str, Dict[str, Any]] = self._build_swatch_lookup()
        self._validate_integrity()

    @property
    def raw_data(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)

    def _build_swatch_lookup(self) -> Dict[str, Dict[str, Any]]:
        out: Dict[str, Dict[str, Any]] = {}
        for fam_id, fam_obj in self._data.get("colour_families", {}).items():
            for name, sw in fam_obj.get("canonical_swatches", {}).items():
                out[name] = {
                    "name": name,
                    "colour_family": fam_id,
                    "canonical_hex": normalize_hex(sw["canonical_hex"]),
                    "accessible_on_light_hex": normalize_hex(sw["accessible_on_light_hex"]),
                    "accessible_on_dark_hex": normalize_hex(sw["accessible_on_dark_hex"]),
                    "preferred_role": sw.get("preferred_role", "foreground"),
                    "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
                }
        return out

    def _validate_integrity(self) -> None:
        # 1. Every rule section must carry a valid evidence_label
        assert_valid_evidence_label(self._data["client_palette_policy"]["evidence_label"])
        assert_valid_evidence_label(self._data["contrast_thresholds"]["evidence_label"])
        assert_valid_evidence_label(self._data["allowed_logo_types_v1"]["evidence_label"])
        assert_valid_evidence_label(self._data["free_scan_verdict_rule"]["evidence_label"])
        assert_valid_evidence_label(self._data["category_norms_layer1"]["evidence_label"])
        assert_valid_evidence_label(self._data["regional_colour_context"]["evidence_label"])

        for gate in self._data["hard_gates_v1"] + self._data["advisory_gates_v1"]:
            assert_valid_evidence_label(gate["evidence_label"])

        for rule in self._data["published_perception_rules"].values():
            assert_valid_evidence_label(rule["evidence_label"])

        for rule in self._data["approved_business_archetype_rules"].values():
            assert_valid_evidence_label(rule["evidence_label"])
            if rule["status"] != "APPROVED":
                raise ValueError(f"Non-approved rule leaked into approved_business_archetype_rules: {rule}")

        for rule in self._data["excluded_draft_archetype_rules"].values():
            assert_valid_evidence_label(rule["evidence_label"])

        # 2. Symbol concepts must cover 1..9, with 2/4/7 strictly NOT_CONFIGURED
        symbols = self._data["symbol_concepts_by_root"]
        if set(symbols.keys()) != {str(n) for n in SINGLE_DIGIT_ROOTS}:
            raise ValueError("symbol_concepts_by_root must contain exact keys '1'..'9'.")
        for n in SINGLE_DIGIT_ROOTS:
            entry = symbols[str(n)]
            assert_valid_evidence_label(entry["evidence_label"])
            if n in (2, 4, 7):
                if entry["status"] != "NOT_CONFIGURED" or entry["symbol_id"] is not None:
                    raise ValueError(f"Root {n} symbol must remain NOT_CONFIGURED until approved.")
            else:
                if entry["status"] != "APPROVED" or not entry["symbol_id"]:
                    raise ValueError(f"Root {n} symbol must be APPROVED with non-empty symbol_id.")

        # 3. Every colour name in NUMBER_REGISTRY[1..9] must exist in _swatch_lookup
        for n in SINGLE_DIGIT_ROOTS:
            reg = NUMBER_REGISTRY[n]
            for cname in list(reg.get("favourable_colours", [])) + list(reg.get("colours_to_avoid", [])):
                if cname not in self._swatch_lookup:
                    raise ValueError(
                        f"NUMBER_REGISTRY[{n}] colour {cname!r} is missing from logo_rules_v1.json colour_families."
                    )

    def get_single_digit_numerology_rule(self, root_number: int) -> Dict[str, Any]:
        """
        Returns the read-only numerology profile for a single-digit root `1..9`,
        including resolved client colour swatches (`D6`: client tables govern navy/black).
        Rejects master numbers (`11, 22, 33`) or out-of-range values.
        """
        if isinstance(root_number, bool) or not isinstance(root_number, int) or root_number not in SINGLE_DIGIT_ROOTS:
            raise ValueError(
                f"Logo Intelligence requires a reduced single-digit root 1..9; got {root_number!r}."
            )
        reg = copy.deepcopy(NUMBER_REGISTRY[root_number])
        fav_swatches = [copy.deepcopy(self._swatch_lookup[c]) for c in reg.get("favourable_colours", [])]
        avoid_swatches = [copy.deepcopy(self._swatch_lookup[c]) for c in reg.get("colours_to_avoid", [])]

        return {
            "root_number": root_number,
            "planet": reg["planet"],
            "element": reg["element"],
            "friendly_numbers": list(reg["friendly_numbers"]),
            "neutral_numbers": list(reg["neutral_numbers"]),
            "enemy_numbers": list(reg["enemy_numbers"]),
            "favourable_days": list(reg["favourable_days"]),
            "favourable_colours": list(reg["favourable_colours"]),
            "colours_to_avoid": list(reg["colours_to_avoid"]),
            "favourable_swatches": fav_swatches,
            "avoid_swatches": avoid_swatches,
            "methodology_id": reg.get("methodology_id", "METH-VEDIC-001"),
            "status": reg.get("status", "APPROVED"),
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    def get_symbol_concept_for_root(self, root_number: int) -> Dict[str, Any]:
        """
        Looks up the Studio symbol concept for root `1..9`.
        Roots `2`, `4`, and `7` strictly return `status="NOT_CONFIGURED"`,
        `display_status="Not configured"`, `symbol_id=None`, `evidence_label="NOT_CONFIGURED"`.
        """
        if isinstance(root_number, bool) or not isinstance(root_number, int) or root_number not in SINGLE_DIGIT_ROOTS:
            raise ValueError(
                f"Symbol concept lookup requires a single-digit root 1..9; got {root_number!r}."
            )
        return copy.deepcopy(self._data["symbol_concepts_by_root"][str(root_number)])

    def check_colour_against_root(self, hex_code: str, root_number: int) -> Dict[str, Any]:
        """
        Checks a client logo HEX colour against `NUMBER_REGISTRY[root_number]`.
        Follows Locked Decision D6: Navy and Black are favourable for Root 8 (Saturn)
        and avoided only for roots whose own numerology table lists them in `colours_to_avoid`.
        """
        profile = self.get_single_digit_numerology_rule(root_number)
        classified = classify_hex_colour_family(hex_code, self._data)
        fam = classified["colour_family"]
        lum = classified["relative_luminance"]
        val = classified["value_hsv"]

        matched_avoid: List[str] = []
        for sw in profile["avoid_swatches"]:
            cname = sw["name"]
            sw_fam = sw["colour_family"]
            if cname == "Dark Green in Business":
                if fam == "green_emerald_mint" and val <= 0.45:
                    matched_avoid.append(cname)
            elif cname == "Dark Yellow":
                if fam == "gold_yellow" and val <= 0.68 and lum <= 0.25:
                    matched_avoid.append(cname)
            elif cname in ("Dark Grey", "Dark Charcoal"):
                if fam in ("grey_silver", "black_charcoal") and val <= 0.35:
                    matched_avoid.append(cname)
            elif sw_fam == fam:
                matched_avoid.append(cname)

        matched_fav: List[str] = []
        if not matched_avoid:
            for sw in profile["favourable_swatches"]:
                if sw["colour_family"] == fam:
                    matched_fav.append(sw["name"])

        if matched_avoid:
            alignment = "AVOID"
        elif matched_fav:
            alignment = "FAVOURABLE"
        else:
            alignment = "NEUTRAL"

        return {
            "hex": classified["hex"],
            "colour_family": fam,
            "root_number": root_number,
            "planet": profile["planet"],
            "alignment": alignment,
            "is_avoided_colour": bool(matched_avoid),
            "is_favourable_colour": bool(matched_fav),
            "matched_avoid_names": matched_avoid,
            "matched_favourable_names": matched_fav,
            "evidence_label": EvidenceLabel.TRADITIONAL_RULE.value,
        }

    def get_archetype_rule_status(self, rule_id: str) -> Dict[str, Any]:
        """Returns approved archetype rule metadata or explicit NOT_CONFIGURED status for draft/unknown IDs."""
        approved = self._data["approved_business_archetype_rules"]
        if rule_id in approved:
            return copy.deepcopy(approved[rule_id])
        return {
            "rule_id": rule_id,
            "status": "NOT_CONFIGURED",
            "display_status": "Not configured",
            "evidence_label": EvidenceLabel.NOT_CONFIGURED.value,
        }

    def get_layer1_category_profile(self, category_id: str, region: str = "INDIA") -> Dict[str, Any]:
        """
        Resolves Layer 1 allowed colour families, allowed shape families, approved-only
        business archetype rules, and regional cultural notes (`INDIA` vs `INTERNATIONAL`).
        Ambiguous or unknown categories return `status="INSUFFICIENT_EVIDENCE"` without guessing.
        """
        reg_key = (region or "INDIA").strip().upper()
        if reg_key not in VALID_REGIONS:
            raise ValueError(f"Unsupported region {region!r}; expected one of {sorted(VALID_REGIONS)}.")

        region_cfg = copy.deepcopy(self._data["regional_colour_context"]["regions"][reg_key])
        cat_key = (category_id or "UNKNOWN").strip().lower()
        categories = self._data["category_norms_layer1"]["categories"]

        if cat_key == "unknown" or cat_key not in categories:
            return {
                "category_id": category_id or "UNKNOWN",
                "status": "INSUFFICIENT_EVIDENCE",
                "allowed_colour_families": [],
                "allowed_shape_families": [],
                "approved_archetypes": [],
                "region": region_cfg,
                "evidence_label": EvidenceLabel.NOT_CONFIGURED.value,
            }

        cat_entry = categories[cat_key]
        approved_map = self._data["approved_business_archetype_rules"]
        approved_archetypes = [
            copy.deepcopy(approved_map[rid])
            for rid in cat_entry.get("approved_archetype_rule_ids", [])
            if rid in approved_map
        ]

        return {
            "category_id": cat_key,
            "status": "RESOLVED",
            "allowed_colour_families": list(cat_entry["allowed_colour_families"]),
            "allowed_shape_families": list(cat_entry["allowed_shape_families"]),
            "approved_archetypes": approved_archetypes,
            "pure_black_category_caution": cat_key in region_cfg.get("caution_categories_for_pure_black", []),
            "region": region_cfg,
            "source_citation": self._data["category_norms_layer1"]["source_citation"],
            "evidence_label": EvidenceLabel.PUBLISHED_RESEARCH.value,
        }

    def derive_shape_and_lightness_guidance(
        self,
        personality_words: List[str],
        price_position: str = "mid",
    ) -> Dict[str, Any]:
        """
        Evaluates published perception rules for brand personality & positioning:
        - Jiang et al. (2016): circular softness/care vs. angular durability/precision
        - Zeng et al.: darker heritage/institutional vs. lighter modern/youthful
        """
        tokens = " ".join(w.strip().lower() for w in (personality_words or []) if w and w.strip())
        pos = (price_position or "mid").strip().lower()

        shape_cfg = self._data["published_perception_rules"]["shape_vs_promise"]
        soft_hits = [kw for kw in shape_cfg["softness_care_keywords"] if kw in tokens]
        hard_hits = [kw for kw in shape_cfg["durability_precision_keywords"] if kw in tokens]

        if soft_hits and not hard_hits:
            recommended_shape = "circular_curved"
        elif hard_hits and not soft_hits:
            recommended_shape = "angular_geometric"
        else:
            recommended_shape = "balanced_hybrid"

        light_cfg = self._data["published_perception_rules"]["lightness_vs_brand_position"]
        dark_hits = [kw for kw in light_cfg["heritage_traditional_keywords"] if kw in tokens]
        light_hits = [kw for kw in light_cfg["modern_youthful_keywords"] if kw in tokens]

        if dark_hits and not light_hits:
            recommended_lightness = "dark_value_range"
        elif light_hits and not dark_hits:
            recommended_lightness = "light_or_medium_value_range"
        elif pos == "premium":
            recommended_lightness = "deep_or_high_contrast_value_range"
        else:
            recommended_lightness = "balanced_medium_value_range"

        return {
            "shape_guidance": {
                "recommended_shape_family": recommended_shape,
                "matched_softness_terms": soft_hits,
                "matched_durability_terms": hard_hits,
                "source_citation": shape_cfg["source_citation"],
                "evidence_label": EvidenceLabel.PUBLISHED_RESEARCH.value,
            },
            "lightness_guidance": {
                "recommended_lightness": recommended_lightness,
                "price_position": pos,
                "matched_heritage_terms": dark_hits,
                "matched_modern_terms": light_hits,
                "source_citation": light_cfg["source_citation"],
                "evidence_label": EvidenceLabel.PUBLISHED_RESEARCH.value,
            },
        }


_SINGLETON_RULEBOOK: Optional[LogoRulebookV1] = None


def get_rulebook_v1() -> LogoRulebookV1:
    global _SINGLETON_RULEBOOK
    if _SINGLETON_RULEBOOK is None:
        _SINGLETON_RULEBOOK = LogoRulebookV1()
    return _SINGLETON_RULEBOOK
