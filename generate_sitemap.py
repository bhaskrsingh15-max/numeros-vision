# -*- coding: utf-8 -*-
"""
generate_sitemap.py
===================
Generates the authoritative sitemap.xml for Numeros Vision (https://numerosvision.com).
Complies with Sitemaps Protocol 0.9, Google Search Console, and Bing Webmaster guidelines.
"""

import os
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# 1. Canonical Core Routes
PRIMARY_ROUTES = [
    ("", "daily", "1.0"),
    ("sample_roadmap/", "weekly", "0.9"),
    ("reports_catalogue/", "weekly", "0.9"),
    ("pricing/", "weekly", "0.9"),
    ("calculators/", "weekly", "0.9"),
    ("charm-ai/", "weekly", "0.9"),
    ("learn/", "monthly", "0.8"),
    ("consultation/", "monthly", "0.8"),
    ("practitioner/", "monthly", "0.8"),
    ("about/", "monthly", "0.8"),
    ("contact/", "monthly", "0.8"),
    ("methodology/", "monthly", "0.8"),
    ("numerology_overview/", "monthly", "0.8"),
    ("insights/", "monthly", "0.8"),
    ("compare/", "monthly", "0.8"),
    ("faq/", "monthly", "0.8"),
    ("signup/", "weekly", "0.85"),
    ("login/", "monthly", "0.7"),
    ("dashboard/", "weekly", "0.8"),
    ("sitemap/", "weekly", "0.8"),
]

# 2. Interactive Discovery Tools (/tools/)
TOOL_ROUTES = [
    ("tools/lo-shu-grid/", "weekly", "0.85"),
    ("tools/name-numerology/", "weekly", "0.85"),
    ("tools/name-balancing/", "weekly", "0.85"),
    ("tools/mobile-numerology/", "weekly", "0.85"),
    ("tools/life-path-calculator/", "weekly", "0.85"),
    ("tools/compatibility-calculator/", "weekly", "0.85"),
    ("tools/business-alignment/", "weekly", "0.85"),
    ("tools/baby-naming/", "weekly", "0.85"),
    ("tools/property-numerology/", "weekly", "0.85"),
    ("tools/vehicle-numerology/", "weekly", "0.85"),
    ("tools/blessing-years/", "weekly", "0.85"),
    ("tools/profession-calculator/", "weekly", "0.85"),
    ("tools/lucky-number/", "weekly", "0.85"),
    ("tools/logo-intelligence/", "weekly", "0.85"),
]

# 3. Dedicated Calculators
CALCULATOR_ROUTES = [
    ("calculators/birth-number/", "weekly", "0.85"),
    ("calculators/lo-shu-grid/", "weekly", "0.85"),
    ("calculators/pythagorean/", "weekly", "0.85"),
]

# 4. Regional & City Hubs
LOCAL_ROUTES = [
    ("local/", "monthly", "0.75"),
    ("local/delhi/", "monthly", "0.75"),
    ("local/mumbai/", "monthly", "0.75"),
    ("local/bangalore/", "monthly", "0.75"),
    ("local/dubai/", "monthly", "0.75"),
]

# 5. Statutory, Legal & Trust Directives
LEGAL_ROUTES = [
    ("privacy/", "monthly", "0.5"),
    ("terms/", "monthly", "0.5"),
    ("refund-policy/", "monthly", "0.5"),
    ("disclaimer/", "monthly", "0.5"),
    ("accessibility/", "monthly", "0.5"),
    ("cookie-policy/", "monthly", "0.5"),
]

# 6. Editorial Knowledge Base (/blog/)
blog_dir = os.path.join("app", "static", "blog")
blog_files = sorted([f for f in os.listdir(blog_dir) if f.endswith(".html") and f != "index.html"])

# Compile XML
xml = ['<?xml version="1.0" encoding="UTF-8"?>']
xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

def add_url(loc, changefreq, priority):
    xml.append(f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>')

for r, freq, prio in PRIMARY_ROUTES:
    add_url(f"https://numerosvision.com/{r}", freq, prio)

for r, freq, prio in TOOL_ROUTES:
    add_url(f"https://numerosvision.com/{r}", freq, prio)

for r, freq, prio in CALCULATOR_ROUTES:
    add_url(f"https://numerosvision.com/{r}", freq, prio)

for r, freq, prio in LOCAL_ROUTES:
    add_url(f"https://numerosvision.com/{r}", freq, prio)

# Blog Index
add_url("https://numerosvision.com/blog/", "weekly", "0.85")

# Individual Blog Articles
for bf in blog_files:
    add_url(f"https://numerosvision.com/blog/{bf}", "monthly", "0.75")

for r, freq, prio in LEGAL_ROUTES:
    add_url(f"https://numerosvision.com/{r}", freq, prio)

xml.append('</urlset>')

out_path = os.path.join("app", "static", "sitemap.xml")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(xml))

total_urls = len(PRIMARY_ROUTES) + len(TOOL_ROUTES) + len(CALCULATOR_ROUTES) + len(LOCAL_ROUTES) + 1 + len(blog_files) + len(LEGAL_ROUTES)
print(f"Successfully generated {out_path} with {total_urls} canonical URLs.")
