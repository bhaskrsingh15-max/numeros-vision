"""
app.seo.anti_penalty_guardrails
Enforces strict compliance with Google Search Essentials, Helpful Content Guidelines,
and Anti-Spam algorithms (SpamBrain, Panda, Penguin, Core Algorithmic Updates).

Guarantees that advanced SEO 'hacks and tricks' remain safely within white-hat boundaries
so the domain maintains long-term organic authority without risking penalties.
"""

import re
import json
from typing import Dict, List, Any, Tuple

class AntiPenaltyGuardrailValidator:
    """Validates HTML content against Google Search Essentials & spam policy limits."""

    @classmethod
    def validate_page_html(cls, html: str, target_keyword: str = "") -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Runs comprehensive anti-penalty checks on generated or existing HTML.
        Returns: (is_compliant, list_of_violations_or_warnings, audit_metrics)
        """
        issues = []
        metrics = {}

        # 1. Title Tag Inspection
        title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        if not title_m:
            issues.append("CRITICAL: Missing <title> tag.")
        else:
            title_text = title_m.group(1).strip()
            metrics["title_length"] = len(title_text)
            if len(title_text) < 25:
                issues.append(f"WARNING: Title too short ({len(title_text)} chars). Optimal: 50-65 chars.")
            elif len(title_text) > 72:
                issues.append(f"WARNING: Title too long ({len(title_text)} chars). Risks truncation in Google SERP.")

        # 2. Meta Description Inspection
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        if not desc_m:
            desc_m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.I)
        if not desc_m:
            issues.append("CRITICAL: Missing meta description tag.")
        else:
            desc_text = desc_m.group(1).strip()
            metrics["description_length"] = len(desc_text)
            if len(desc_text) < 110:
                issues.append(f"WARNING: Meta description too short ({len(desc_text)} chars). Optimal: 140-160.")
            elif len(desc_text) > 175:
                issues.append(f"WARNING: Meta description too long ({len(desc_text)} chars). Google may truncate.")

        # 3. Canonical Tag Verification
        canon_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.I)
        if not canon_m or not canon_m.group(1).strip().startswith("https://"):
            issues.append("CRITICAL: Missing or invalid HTTPS canonical tag (causes duplicate content confusion).")

        # 4. Heading Hierarchy & Single H1 Rule
        h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        metrics["h1_count"] = len(h1_matches)
        if len(h1_matches) == 0:
            issues.append("CRITICAL: Missing <h1> tag. Primary topical anchor missing.")
        elif len(h1_matches) > 1:
            issues.append(f"PENALTY RISK: Multiple <h1> tags ({len(h1_matches)}). Confuses Google topic clustering.")

        # 5. Keyword Stuffing Guardrail (Safe Density: 1.0% - 2.5%)
        # Strip script and style tags before calculating text density
        clean_text = re.sub(r"<script.*?</script>", " ", html, flags=re.I | re.S)
        clean_text = re.sub(r"<style.*?</style>", " ", clean_text, flags=re.I | re.S)
        clean_text = re.sub(r"<[^>]+>", " ", clean_text)
        words = [w for w in re.findall(r"\w+", clean_text.lower()) if len(w) > 2]
        total_words = len(words)
        metrics["total_words"] = total_words

        if target_keyword and total_words > 100:
            kw_words = target_keyword.lower().split()
            # Count target phrase occurrences
            kw_pattern = re.escape(target_keyword.lower())
            occurrences = len(re.findall(kw_pattern, clean_text.lower()))
            # Density percentage based on word counts
            density = (occurrences * len(kw_words) / total_words) * 100
            max_safe = 3.5 if len(kw_words) > 2 else 2.8
            if density > max_safe:
                issues.append(f"PENALTY RISK (KEYWORD STUFFING): Density is {density:.2f}% (safe limit is <= {max_safe}%).")
            elif density < 0.3 and total_words > 400:
                issues.append(f"WARNING (LOW TOPICAL FOCUS): Target keyword density is only {density:.2f}%.")

        # 6. Hidden Text / Black-Hat CSS Cloaking Guardrail
        # Distinguish between valid UI styles and deceptive text hiding (e.g. 0px text)
        deceptive_hidden_patterns = [
            r"font-size\s*:\s*0(?:\.0+)?(?:px|pt)?\s*(?:;|\"|\'|!)(?![\.\d])",
            r"text-indent\s*:\s*-\d{4,}px",
            r"position\s*:\s*absolute;\s*left\s*:\s*-\d{4,}px",
            r"color\s*:\s*transparent"
        ]
        for pat in deceptive_hidden_patterns:
            matches = re.findall(r"<(?:p|span|div|a|h\d)[^>]*style=[\"'][^\"']*" + pat, html, re.I)
            if matches:
                issues.append(f"PENALTY RISK (CLOAKING / DECEPTIVE TEXT): Found black-hat pattern '{pat}'.")

        # 7. Valid Schema.org Structured Data
        schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', html, re.I | re.S)
        metrics["schema_count"] = len(schema_matches)
        if len(schema_matches) == 0:
            issues.append("WARNING: Missing JSON-LD structured data. Loses rich snippet & AEO advantage.")
        else:
            for s_str in schema_matches:
                try:
                    s_data = json.loads(s_str.strip())
                    if "@context" not in s_data and "@graph" not in s_data:
                        issues.append("WARNING: JSON-LD missing Schema.org @context.")
                except Exception as e:
                    issues.append(f"CRITICAL: Broken JSON-LD syntax: {e}")

        # 8. App Store / PWA Compliance
        if 'rel="manifest"' not in html:
            issues.append("PWA GAP: Missing manifest.json link for App Store / PWA discoverability.")
        if 'name="apple-mobile-web-app-capable"' not in html:
            issues.append("PWA GAP: Missing Apple mobile web app tags.")

        # 9. Technical Security / Stealth Check (Zero tech stack leakage)
        leakage = re.findall(r"\b(owasp\s+hardened|owasp\s+waf|fastapi|uvicorn|supabase|postgresql\s+schema)\b", html, re.I)
        if leakage:
            issues.append(f"SECURITY GAP: Tech stack leakage detected: {set(leakage)}")

        is_compliant = not any("CRITICAL" in i or "PENALTY RISK" in i or "SECURITY GAP" in i for i in issues)
        return is_compliant, issues, metrics
