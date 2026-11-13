"""
app.seo.ranking_scanner
Automated Search Engine Ranking & Competitiveness Scanner.

Emulates Googlebot crawlers to scan all site pages and evaluate:
1. Googlebot crawl latency (TTFB) & HTTP status
2. Title & Meta Description CTR potential
3. Semantic Content Depth & LSI Entity Co-occurrence
4. AEO & GEO Featured Snippet / Zero-Click Readiness
5. Schema.org JSON-LD structured data richness
6. Technical Core Web Vitals & PWA / Mobile Readiness
7. SERP Rank Potential Prediction (Tier 1: Page 1, Tier 2: Top 20, Tier 3: Needs Tuning)
"""

import os
import re
import time
import json
import urllib.request
from typing import Dict, List, Any

# Target keyword mapping for each public page
PAGE_KEYWORD_MAP: Dict[str, str] = {
    "/": "AI numerology calculator",
    "/about": "numerology research board",
    "/pricing": "numerology consultation pricing",
    "/contact": "numerology support consultation",
    "/privacy": "numerology privacy data governance",
    "/terms": "numerology terms of service",
    "/refund-policy": "numerology refund policy",
    "/practitioner": "practitioner numerology portal",
    "/sample": "sample numerology blueprint report",
    "/tools/name-balancing": "name balancing calculator",
    "/tools/mobile-numerology": "mobile numerology audit",
    "/tools/blessing-years": "blessing years timeline",
    "/tools/profession-calculator": "career profession numerology",
    "/tools/vehicle-numerology": "vehicle numerology audit",
    "/tools/compatibility-calculator": "relationship marriage compatibility",
    "/tools/property-numerology": "house property numerology",
    "/tools/baby-naming": "auspicious baby naming",
    "/tools/life-path-calculator": "life path number calculator",
    "/tools/lo-shu-grid": "lo shu grid calculator",
    "/tools/lucky-number": "lucky number calculator",
    "/tools/name-numerology": "chaldean name numerology",
    "/blog/what-is-numerology": "what is numerology",
    "/blog/master-numbers-11-22-33": "master numbers 11 22 33",
    "/blog/chaldean-vs-pythagorean-numerology": "chaldean vs pythagorean numerology",
    "/blog/lo-shu-grid-8-planes": "lo shu grid 8 planes",
    "/blog/mobile-numerology-malefic-pairs": "mobile numerology malefic pairs",
    "/blog/life-path-numbers-explained": "life path numbers explained",
    "/blog/gemstone-remedies": "gemstone crystal remedies numerology",
    "/blog/vedic-gemstone-remedies": "vedic gemstone remedies",
    "/blog/kua-number-auspicious-directions-and-career-feng-shui": "kua number auspicious directions"
}

class RankingScanner:
    """Automated crawler that scores pages for search engine ranking readiness."""

    @classmethod
    def scan_page(cls, base_url: str, path: str, target_kw: str) -> Dict[str, Any]:
        """Scans a single URL emulating Googlebot and calculates its ranking score."""
        full_url = f"{base_url.rstrip('/')}{path}"
        req = urllib.request.Request(
            full_url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            }
        )

        t_start = time.time()
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                ttfb_ms = round((time.time() - t_start) * 1000, 1)
                status_code = resp.getcode()
                html = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            return {
                "path": path,
                "url": full_url,
                "status": "ERROR",
                "error": str(e),
                "rank_score": 0,
                "tier": "Offline"
            }

        # ── 1. Title Analysis (Max 20 pts) ──
        title_score = 0
        title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        title_text = title_m.group(1).strip() if title_m else ""
        if title_text:
            title_score += 8  # Title exists
            if 45 <= len(title_text) <= 70:
                title_score += 6  # Optimal length
            elif 30 <= len(title_text) <= 80:
                title_score += 3
            # Check target keyword match
            kw_tokens = [t for t in target_kw.lower().split() if len(t) > 2]
            if any(t in title_text.lower() for t in kw_tokens):
                title_score += 4
            if "numeros vision" in title_text.lower() or "charm ai" in title_text.lower():
                title_score += 2  # Brand authority anchor

        # ── 2. Meta Description Analysis (Max 15 pts) ──
        desc_score = 0
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        if not desc_m:
            desc_m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.I)
        desc_text = desc_m.group(1).strip() if desc_m else ""
        if desc_text:
            desc_score += 6
            if 135 <= len(desc_text) <= 165:
                desc_score += 5
            elif 100 <= len(desc_text) <= 200:
                desc_score += 3
            if any(t in desc_text.lower() for t in kw_tokens):
                desc_score += 4

        # ── 3. Heading Structure (Max 15 pts) ──
        heading_score = 0
        h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.I | re.S)
        h3s = re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.I | re.S)

        if len(h1s) == 1:
            heading_score += 7  # Exactly 1 H1
            if any(t in h1s[0].lower() for t in kw_tokens):
                heading_score += 3  # H1 keyword focus
        if len(h2s) >= 2:
            heading_score += 3
        if len(h3s) >= 2:
            heading_score += 2

        # ── 4. Content Depth & Topical Relevance (Max 20 pts) ──
        content_score = 0
        clean_text = re.sub(r"<script.*?</script>", " ", html, flags=re.I | re.S)
        clean_text = re.sub(r"<style.*?</style>", " ", clean_text, flags=re.I | re.S)
        clean_text = re.sub(r"<[^>]+>", " ", clean_text)
        words = [w for w in re.findall(r"\w+", clean_text.lower()) if len(w) > 2]
        total_words = len(words)

        if total_words >= 1000:
            content_score += 10
        elif total_words >= 500:
            content_score += 7
        elif total_words >= 250:
            content_score += 5
        else:
            content_score += 2

        # Safe density check
        kw_pattern = re.escape(target_kw.lower())
        occurrences = len(re.findall(kw_pattern, clean_text.lower()))
        density = (occurrences * len(target_kw.split()) / max(total_words, 1)) * 100
        if 0.5 <= density <= 2.5:
            content_score += 5
        elif density > 2.8:
            content_score -= 5  # Stuffing penalty deduction
        else:
            content_score += 3

        # LSI terms presence
        lsi_found = sum(1 for w in ["planetary", "vibration", "energy", "vedic", "matrix", "remedy", "lo shu", "harmony"] if w in clean_text.lower())
        content_score += min(lsi_found, 5)

        # ── 5. AEO & GEO Snippet Readiness (Max 15 pts) ──
        aeo_score = 0
        if '<aside class="snippet-box">' in html or 'class="snippet-box"' in html or 'role="region"' in html:
            aeo_score += 5  # Snippet bait box
        if "<table" in html:
            aeo_score += 4  # Structured matrix for AI overviews
        if 'class="faq-item"' in html or 'itemtype="https://schema.org/FAQPage"' in html:
            aeo_score += 4  # FAQ accordion
        if "<ul" in html or "<ol" in html:
            aeo_score += 2  # Structured lists

        # ── 6. Schema.org & Technical PWA (Max 15 pts) ──
        tech_score = 0
        if '<script type="application/ld+json">' in html or "<script type='application/ld+json'>" in html:
            tech_score += 6
        if 'rel="canonical"' in html and 'https://numerosvision.com' in html:
            tech_score += 3
        if 'name="robots"' in html and 'max-image-preview:large' in html:
            tech_score += 2
        if 'rel="manifest"' in html and 'manifest.json' in html:
            tech_score += 2
        if 'name="apple-mobile-web-app-capable"' in html:
            tech_score += 2

        total_score = min(100, title_score + desc_score + heading_score + content_score + aeo_score + tech_score)

        if total_score >= 88:
            tier = "Tier 1: High Page 1 Potential"
        elif total_score >= 75:
            tier = "Tier 2: Strong Top 10-20 Contender"
        else:
            tier = "Tier 3: Optimization Recommended"

        recommendations = []
        if len(h1s) != 1:
            recommendations.append("Ensure exactly one <h1> tag is present.")
        if not (45 <= len(title_text) <= 70):
            recommendations.append(f"Adjust title length ({len(title_text)} chars) to 50-65 chars.")
        if not (135 <= len(desc_text) <= 165):
            recommendations.append(f"Adjust meta description ({len(desc_text)} chars) to 140-160 chars.")
        if aeo_score < 10:
            recommendations.append("Add direct-answer snippet bait box or FAQ schema to capture Position Zero.")
        if total_words < 600 and "tools" not in path:
            recommendations.append(f"Expand word count (currently {total_words}) to compete with Page 1 average.")

        return {
            "path": path,
            "url": full_url,
            "target_keyword": target_kw,
            "status_code": status_code,
            "ttfb_ms": ttfb_ms,
            "total_words": total_words,
            "title_length": len(title_text),
            "meta_desc_length": len(desc_text),
            "h1_count": len(h1s),
            "h2_count": len(h2s),
            "score_breakdown": {
                "title": title_score,
                "meta_description": desc_score,
                "headings": heading_score,
                "content_depth": content_score,
                "aeo_geo_snippets": aeo_score,
                "schema_and_technical": tech_score
            },
            "rank_readiness_score": total_score,
            "predicted_serp_tier": tier,
            "recommendations": recommendations
        }

    @classmethod
    def scan_all_pages(cls, base_url: str = "http://127.0.0.1:8000") -> Dict[str, Any]:
        """Scans all registered site pages and produces a master ranking readiness report."""
        results = []
        scores = []

        for path, target_kw in PAGE_KEYWORD_MAP.items():
            res = cls.scan_page(base_url, path, target_kw)
            results.append(res)
            if res.get("rank_readiness_score"):
                scores.append(res["rank_readiness_score"])

        avg_score = round(sum(scores) / max(len(scores), 1), 1)
        tier1_count = sum(1 for r in results if "Tier 1" in r.get("predicted_serp_tier", ""))
        tier2_count = sum(1 for r in results if "Tier 2" in r.get("predicted_serp_tier", ""))
        tier3_count = sum(1 for r in results if "Tier 3" in r.get("predicted_serp_tier", ""))

        summary = {
            "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_pages_scanned": len(results),
            "average_rank_readiness_score": avg_score,
            "tier_distribution": {
                "tier_1_page_1_potential": tier1_count,
                "tier_2_top_20_contenders": tier2_count,
                "tier_3_needs_tuning": tier3_count
            },
            "pages": results
        }

        # Persist report to data/
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        os.makedirs(data_dir, exist_ok=True)
        report_path = os.path.join(data_dir, "seo_ranking_audit.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        summary["saved_to"] = report_path
        return summary
