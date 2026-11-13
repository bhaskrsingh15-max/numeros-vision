"""
Update pricing.html and reports_catalogue.html to Global English-Only Standards
"""
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def update_pricing_html():
    filepath = os.path.join(ROOT_DIR, "app", "static", "pricing.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update DOMAIN_DATA.core
    # tripwire -> Basic Numerology Report
    # master -> Advanced Numerology Report
    # sovereign -> Premium Numerology Report
    content = content.replace(
        "tripwire: { name: 'Rapid Diagnostic Action Plan', price: '₹199', strike: '₹410', note: '3-Page Personal Blueprint &amp; Vitality Overview · Instant PDF' },",
        "tripwire: { name: 'Basic Numerology Report', price: '₹199', strike: '₹410', note: 'A concise report presenting your calculated results, the method used and an initial interpretation of the key findings.' },"
    )
    content = content.replace(
        "master:   { name: '12-Page Complete Life Dossier', price: '₹510', strike: '₹1,500', note: '12-Page Complete Life Trajectory &amp; 5-Year Dasha' },",
        "master:   { name: 'Advanced Numerology Report', price: '₹510', strike: '₹1,500', note: 'A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product.' },"
    )
    content = content.replace(
        "sovereign:{ name: 'Imperial Sovereign Blueprint', price: '₹1,050', strike: '₹2,500', note: 'Comprehensive Detailed Report &amp; 10-Year Radar' }",
        "sovereign:{ name: 'Premium Numerology Report', price: '₹1,050', strike: '₹2,500', note: 'An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product.' }"
    )

    # USD equivalents
    content = content.replace(
        "tripwire: { name: 'Rapid Diagnostic Action Plan', price: '$5.00', strike: '$15.00', note: '3-Page Personal Blueprint &amp; Vitality Overview' },",
        "tripwire: { name: 'Basic Numerology Report', price: '$5.00', strike: '$15.00', note: 'A concise report presenting your calculated results, the method used and an initial interpretation of the key findings.' },"
    )
    content = content.replace(
        "master:   { name: '12-Page Complete Life Dossier', price: '$14.00', strike: '$45.00', note: '12-Page Complete Life Trajectory &amp; 5-Year Dasha' },",
        "master:   { name: 'Advanced Numerology Report', price: '$14.00', strike: '$45.00', note: 'A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product.' },"
    )
    content = content.replace(
        "sovereign:{ name: 'Imperial Sovereign Blueprint', price: '$28.00', strike: '$75.00', note: 'Comprehensive Detailed Report &amp; 10-Year Radar' }",
        "sovereign:{ name: 'Premium Numerology Report', price: '$28.00', strike: '$75.00', note: 'An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product.' }"
    )

    # 2. Update subject-specific variants in DOMAIN_DATA
    # union: Basic Compatibility Report, Advanced Compatibility Report, Premium Compatibility Report
    content = content.replace("name: 'Marital Harmony Gap Unblocker'", "name: 'Basic Compatibility Report'")
    content = content.replace("name: 'Sacred Union & Luxury Dossier'", "name: 'Advanced Compatibility Report'")
    content = content.replace("name: 'Sovereign Couple Destiny Blueprint'", "name: 'Premium Compatibility Report'")

    # commerce: Basic Business Name Report, Advanced Business Name Report, Premium Business Name Report
    content = content.replace("name: 'Cash Flow Gap & Velocity Unblocker'", "name: 'Basic Business Name Report'")
    content = content.replace("name: 'Commercial Mastery Dossier'", "name: 'Advanced Business Name Report'")
    content = content.replace("name: 'Enterprise Scaling & Brand Matrix'", "name: 'Premium Business Name Report'")

    # authority: Basic Life Path Report, Advanced Life Path Report, Premium Life Path Report
    content = content.replace("name: 'Career Authority Gap Unblocker'", "name: 'Basic Life Path Report'")
    content = content.replace("name: 'Sovereign Leadership Dossier'", "name: 'Advanced Life Path Report'")
    content = content.replace("name: 'Sovereign Identity & Name Rectification'", "name: 'Premium Life Path Report'")

    # relocation & dharma
    content = content.replace("name: 'International Visa & Travel Unblocker'", "name: 'Basic Relocation Numerology Report'")
    content = content.replace("name: 'Global Settlement Dossier'", "name: 'Advanced Relocation Numerology Report'")
    content = content.replace("name: 'Sovereign Global Migration Matrix'", "name: 'Premium Relocation Numerology Report'")

    content = content.replace("name: 'Dharma Compass & Purpose Unblocker'", "name: 'Basic Life Purpose Report'")
    content = content.replace("name: 'Sovereign Wisdom Dossier'", "name: 'Advanced Life Purpose Report'")
    content = content.replace("name: 'Karmic Destiny & Life Blueprint'", "name: 'Premium Life Purpose Report'")

    # 3. Update CTA buttons in renderPricing():
    # Sovereign button:
    content = content.replace(
        '<a href="/#plans" class="btn-gold-action">ANVEIL EVERY CHARM ✦ Get Blueprint (${prices.sovereign.price})</a>',
        '<a href="/#plans" class="btn-gold-action">View Premium Report (${prices.sovereign.price})</a>'
    )
    # Master button:
    content = content.replace(
        '<a href="/#plans" class="btn-gold-action" style="font-weight:700;">ANVEIL EVERY CHARM ✦ Activate Master Dossier (${prices.master.price}) →</a>',
        '<a href="/#plans" class="btn-gold-action" style="font-weight:700;">Explore Advanced Analysis (${prices.master.price}) →</a>'
    )
    # Tripwire button:
    content = content.replace(
        '<a href="/#plans" class="btn-gold-action">Get Gap Remedies (${prices.tripwire.price})</a>',
        '<a href="/#plans" class="btn-gold-action">View Basic Report (${prices.tripwire.price})</a>'
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/static/pricing.html successfully.")

def update_reports_catalogue():
    filepath = os.path.join(ROOT_DIR, "app", "static", "reports_catalogue.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Standardize concept terminology & CTA buttons
    content = content.replace("Discover My Numbers ✦", "View Free Calculation ✦")
    content = content.replace("Get Report ✦", "View Basic Report ✦")
    content = content.replace("Explore Blueprint →", "Explore Advanced Analysis →")
    content = content.replace("Order Dossier →", "View Premium Report →")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/static/reports_catalogue.html successfully.")

if __name__ == "__main__":
    update_pricing_html()
    update_reports_catalogue()
