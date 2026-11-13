# -*- coding: utf-8 -*-
import sys

path = 'app/services/pdf_report_generator.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    (
        '("Section 10: Methodology, Algorithmic Provenance & Statutory Sign-off", "Page 12")',
        '("Section 10: Methodology, Authentic Standards & Ethical Guidance", "Page 12")'
    ),
    (
        '("Section 10: Methodology & Algorithmic Provenance", "Page 12")',
        '("Section 10: Methodology & Authentic Standards", "Page 12")'
    ),
    (
        '[Paragraph("<b>Report Cryptographic ID</b>", s[\'MetaLabel\']), Paragraph(f": {d[\'report_id\']}", s[\'MetaValue\'])],',
        '[Paragraph("<b>Report Verification ID</b>", s[\'MetaLabel\']), Paragraph(f": {d[\'report_id\']}", s[\'MetaValue\'])],'
    ),
    (
        '[Paragraph("<b>Verification Standard</b>", s[\'MetaLabel\']), Paragraph(": Deterministic Python Core v2.2.0 · DPDP 2023 Statutory Compliance", s[\'MetaValue\'])],',
        '[Paragraph("<b>Verification Standard</b>", s[\'MetaLabel\']), Paragraph(": Authentic Numerology Matrix · Verified & Confidential", s[\'MetaValue\'])],'
    ),
    (
        '<b>Notice of Rigorous Provenance:</b> This publication is compiled directly from the birth coordinates of <b>{d[\'seeker_name\']}</b>. All arithmetic reductions, planetary dasha epicycles, and Lo Shu grid geometries are generated deterministically. Traditional numerological interpretations provide strategic life insights with zero fatalism. Consult accredited counsel for legal or medical decisions.',
        '<b>Authentic Methodology Notice:</b> This personalized publication is calculated directly from the birth coordinates of <b>{d[\'seeker_name\']}</b>. All number calculations, dasha cycles, and Lo Shu grid mappings follow classical numerology standards. Interpretations provide positive, practical life insights without fatalism or superstition. Consult accredited professionals for legal or medical advice.'
    ),
    (
        '[Paragraph("<b>Mathematical Vector</b>", s[\'TableHeader\']), Paragraph("<b>Formula & Provenance</b>", s[\'TableHeader\']), Paragraph("<b>Calculated Value & Significance</b>", s[\'TableHeader\'])],',
        '[Paragraph("<b>Core Parameter</b>", s[\'TableHeader\']), Paragraph("<b>Formula & Method</b>", s[\'TableHeader\']), Paragraph("<b>Calculated Value & Significance</b>", s[\'TableHeader\'])],'
    ),
    (
        '<b>Engine Provenance Standard:</b> Compiled deterministically by Numeros Vision Calculation Engine. Chaldean name vibration 32/5 acts as an organic catalyst for high-growth executive leadership.',
        '<b>Calculation Standard:</b> Calculated precisely as per classical Chaldean principles. Your calling name vibration 32/5 acts as a natural positive catalyst for high-growth leadership.'
    ),
    (
        'Section 10: Methodology, Algorithmic Provenance & Governance',
        'Section 10: Methodology, Authentic Standards & Ethical Guidance'
    ),
    (
        '[Paragraph("<b>Governance Dimension</b>", s[\'TableHeader\']), Paragraph("<b>Authoritative Standard & Provenance</b>", s[\'TableHeader\'])],',
        '[Paragraph("<b>Guidance Dimension</b>", s[\'TableHeader\']), Paragraph("<b>Authentic Standard & Method</b>", s[\'TableHeader\'])],'
    ),
    (
        '[Paragraph("Calculation Engine", s[\'TableCell\']), Paragraph("Deterministic Python Core (v2.2.0-release.2026.11) — Zero LLM arithmetic.", s[\'TableCell\'])],',
        '[Paragraph("Calculation Core", s[\'TableCell\']), Paragraph("Classical Vedic & Chaldean mathematical canons with verified accuracy.", s[\'TableCell\'])],'
    ),
    (
        '[Paragraph("Cryptographic Fingerprint", s[\'TableCell\']), Paragraph(f"Report ID: {d[\'report_id\']} | Hash: SHA-256 Verified", s[\'TableCell\'])],',
        '[Paragraph("Digital Verification", s[\'TableCell\']), Paragraph(f"Report ID: {d[\'report_id\']} | Verified & Authentic", s[\'TableCell\'])],'
    ),
    (
        'Traditional frameworks offer psychological, archetypal, and strategic insight. No deterministic claims of commercial success are guaranteed.',
        'Traditional numerology offers personal self-awareness, timing insights, and positive lifestyle guidance. It does not replace medical, legal, or financial professional counsel.'
    ),
    (
        'Master Numerologist Bhaskr Singh (Numeros Vision) · Numeros Vision Algorithmic Council',
        'Master Numerologist Bhaskr Singh (Numeros Vision) · Numeros Vision Advisory Board'
    ),
    (
        'Submit every candidate trademark through our deterministic Chaldean engine',
        'Submit every candidate trademark through our authentic Chaldean calculations'
    )
]

count = 0
for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        count += 1
    else:
        # Check normalized
        old_n = old.replace('\r\n', '\n')
        text_n = text.replace('\r\n', '\n')
        if old_n in text_n:
            text = text_n.replace(old_n, new)
            count += 1
        else:
            print(f"Warning: Not found: {old[:50]}...")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Successfully applied {count}/{len(replacements)} replacements in pdf_report_generator.py")
