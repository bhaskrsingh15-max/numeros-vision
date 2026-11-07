"""
NUMEROS VISION — SOURCE PRIVACY, PROVENANCE OBFUSCATION & IP PROTECTION SHIELD
Strictly locks and sanitizes all knowledge base citations, RAG excerpts, AI LLM prompts,
and API responses. Ensures NO external authors, book titles, training documents,
file extensions (.pdf, .docx, .xlsx), or client case names are EVER exposed
in the frontend, backend APIs, LLM generations, SEO, AEO, or GEO outputs.
"""

import re
import hashlib
from typing import Dict, Any, List, Optional, Union

# Proprietary Master Registry mapping raw ingested files to Sovereign Numeros Vision designations
SOURCE_PROPRIETARY_MAPPING: Dict[str, str] = {
    # Master Classical & Authoritative Treatises
    "numerology Numeros Vision Classical Methodology .pdf": "Numeros Vision Hermetic Core Archive (NV-HCA-01)",
    "Numerology by Numeros Vision Classical Methodology Welcome Kit.pdf": "Numeros Vision Applied Numerology Ledger (NV-ANL-02)",
    "The Ultimate Guide to Numerology Use_.(1).pdf": "Numeros Vision Master Numerological Matrix (NV-MNM-03)",
    "Numerology (Classical Vedic Tradition) (Z-Library).pdf": "Numeros Vision Classical Ayurvedic Numerology Compendium (NV-ANC-04)",
    "Numerology (Vedic Mathematical Tradition) (Z-Library).pdf": "Numeros Vision Vedic Mathematical Treatises (NV-VMT-05)",
    "Numerology the Complete Guide, Volume 1-The Personality Reading.pdf": "Numeros Vision Personality Archetype Canon (NV-PAC-06)",
    "Cheiro's Book of Numbers (English Edition, 1935)": "Numeros Vision Chaldean Harmonic Archive (NV-CHA-07)",
    "Cheiros_Book_of_Numbers_Study_Notes.docx": "Numeros Vision Chaldean Mathematical Notes (NV-CMN-07B)",
    "THE BOOK OF NAKSHATRAS.pdf": "Numeros Vision Stellar Constellation Resonance Canon (NV-SCRC-08)",
    "Vedic Astrology (Classical Astrological Framework) .pdf": "Numeros Vision Vedic Astrological Framework (NV-VAF-09)",
    "Basic Numerology Course - Talking Nummbers.pdf": "Numeros Vision Foundational Vibrational Courseware (NV-FVC-10A)",
    "Basic Numerology Course - Talking Nummbers.hindi.pdf": "Numeros Vision Foundational Vibrational Courseware (NV-FVC-10B)",
    "Advanced_Numerology_Course_Guide___PDF___Devi___Prayer.pdf": "Numeros Vision Advanced Metaphysical Research (NV-AMR-11A)",
    "Advanced_Numerology_Study_Notes___PDF.pdf": "Numeros Vision Advanced Metaphysical Research (NV-AMR-11B)",
    "NP-Karmic-Empowerment-With-Numerology_.pdf": "Numeros Vision Karmic Matrix & Evolution Canon (NV-KME-12)",
    "Professional Numerology Pro Syllabus (Master Notes)": "Numeros Vision Professional Practitioner Curriculum (NV-PPC-13A)",
    "Professional Numerology notes.pdf": "Numeros Vision Professional Practitioner Curriculum (NV-PPC-13B)",
    "Professional_Numerology_Notes_EDITABLE_TABLES.docx": "Numeros Vision Professional Practitioner Curriculum (NV-PPC-13C)",
    "Numeros Vision Brand Blueprint.docx": "Numeros Vision Institutional Brand Architecture (NV-IBA-14)",

    # Combinations & Number Archetypes
    "81 Driver-Conductor Combinations in Numerology PDF Planets In Astrology Wisdom.pdf": "Numeros Vision 81-Matrix Planetary Dynamics (NV-MPD-15)",
    "Mulank and Bhagyank Predictions Guide PDF Psychology Behavioural Sciences.pdf": "Numeros Vision Driver-Conductor Predictive Synthesis (NV-DCPS-16)",
    "Traits and Insights of Numerology 1 PDF Leadership Physical Attractiveness.pdf": "Numeros Vision Monadic Archetype Monograph (NV-MAM-17)",
    "Traits of Number 1 in Vedic Numerology PDF.pdf": "Numeros Vision Solar Planetary Monograph (NV-SPM-18)",
    "Understanding Mulank 1 in Numerology PDF Leadership Creativity.pdf": "Numeros Vision Core Root Vibrational Series (NV-CRVS-19)",
    "Understanding Name Numbers in Numerology PDF Luck Planets.pdf": "Numeros Vision Phonetic Name Valuation Matrix (NV-PNVM-20)",
    "Understanding_Name_Numerology_Numbers___PDF.pdf": "Numeros Vision Name Harmonic Analysis Vault (NV-NHAV-21)",
    "Understanding_Compound_Numbers_in_Numerology___PDF___Luck.pdf": "Numeros Vision Compound Vibrational Archetypes (NV-CVA-21B)",
    "Understanding Numerology Numbers 1-9 PDF.pdf": "Numeros Vision Ninefold Harmonic Continuum (NV-NHC-22A)",
    "NumerologyRepetitiveNos1-9_updated.pdf": "Numeros Vision Repetitive Number Harmonic Matrix (NV-RNHM-22B)",
    "Comprehensive Guide to Numerology Insights PDF Fruit Foods.pdf": "Numeros Vision Elemental Dietary & Lifestyle Alignments (NV-EDLA-23)",
    "Planet details in depth.pdf": "Numeros Vision Celestial Planetary Significations (NV-CPS-24)",
    "Profession, Business, and Education Mastery Class 10 _ PDF _ Planets In Astrology _ Hindu Astrology.pdf": "Numeros Vision Vocational Mastery & Dharma Matrix (NV-VMDM-25)",
    "Calculating Mahadasha in Vedic Astrology PDF Planets In Astrology Self-Improvement.pdf": "Numeros Vision Temporal Chronology & Dasha Cycles (NV-TCDC-26)",
    "RIL_2025_Validated_Numerology_Output.xlsx": "Numeros Vision Empirical Case Validation Index (NV-ECVI-27)",

    # Crystals, Minerals & Remedial Compendiums
    "The_Complete_Guide_to_Crystal_Astrology_360_Crystals_and_Sabian.pdf": "Numeros Vision Mineral Frequency & Sabian Resonance System (NV-MFSR-28)",
    "25 astrological remedies all in one  (1)_compressed.pdf": "Numeros Vision Planetary Harmonization & Remedy Protocols (NV-PHRP-29A)",
    "25-Astrology-remedies-kit-io2rbv.pdf": "Numeros Vision Elemental Alignment Formulary (NV-EAF-29B)",
    "Numerology Insights and Remedies Report PDF Luck.pdf": "Numeros Vision Remedial Balancing Synthesis (NV-RBS-30)",

    # Lo Shu & Spatial Resonance
    "Lo Shu Grid Analysis and Remedies PDF Planets In Astrology Intuition.pdf": "Numeros Vision Lo Shu Grid Energy Vector Framework (NV-LSEV-31A)",
    "Lo shu grid.pdf": "Numeros Vision Lo Shu Grid Planetary Vectors (NV-LSPV-31B)",
    "Practical_Vaastu_Insights_and_Applications___PDF___Basement.pdf": "Numeros Vision Spatial Geometrical Resonance Canon (NV-SGRC-32A)",
    "Vastu_Planning_and_Design_Steps___PDF.pdf": "Numeros Vision Architectural Harmonization Blueprint (NV-AHB-32B)",

    # Specialized Naming & Assets
    "Name Spelling Correction Insights PDF Language Arts & Discipline.pdf": "Numeros Vision Chaldean Name Balancing Corpus (NV-CNBC-33)",
    "Chaldean Numerology Name Analysis PDF Sports & Recreation Wellness.pdf": "Numeros Vision Phonetic & Vibrational Matrix (NV-PVM-34)",
    "BabyNamingNumerology_2026-09-08.pdf": "Numeros Vision Auspicious Natal Phonetics Engine (NV-ANPE-35)",
    "BUSINESS NAME GENERATOR TOOL.docx": "Numeros Vision Enterprise Valuation & Naming Matrix (NV-EVNM-36A)",
    "BRAND NAME -PROMPT.docx": "Numeros Vision Commercial Brand Harmonization Ledger (NV-CBHL-36B)",
    "Vehicle Number Luck Analysis PDF.pdf": "Numeros Vision Kinetic Asset Frequency Index (NV-KAFI-37)",
    "Mobile_Numerology_Master_Sheet___PDF___Marriage.pdf": "Numeros Vision Digital Telecommunication Resonance Canon (NV-DTRC-38A)",
    "Numerology-Based_Mobile_Wallpapers___PDF.pdf": "Numeros Vision Visual Geometry & Wallpaper Vibrations (NV-VGWV-38B)",

    # Verified Diagnostic Consultation Archives (Sanitized Cases)
    "Bhaskr_Singh_numerology.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-01)",
    "Bhaskr_Singh_short_report.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-02)",
    "Ummika_Singh_numerology.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-03)",
    "Ummika_Singh_short_report.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-04)",
    "Kaashvi_Singh_numerology.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-05)",
    "Kaashvi_Singh_short_report.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-06)",
    "Ankur_Sachdeva__numerology.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-07)",
    "Ankur_Sachdeva_short_report.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-08)",
    "Shally_Sharma_short_report.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-09)",
    "serve-me-my-success-bhaskr singh-28-11-1981.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-10)",
    "ummika-singh_name_balancing_report_2026-09-08.pdf": "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-11)",

    # Classical Astrological Syntheses
    "Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise.md": "Numeros Vision Nadi Planetary Conjunctions Canon (NV-NPCC-40)",
    "Midas_Touch_Astrology_of_Wealth_Markdown_Study_Edition.md": "Numeros Vision Wealth & Abundance Astrological Synthesis (NV-WAAS-41)",
    "Market Correlation Engine: NumeroBuilder Benchmark": "Numeros Vision Empirical Benchmark Analytics (NV-EBA-42)",
    "You and Your Name (Know Your Fortune Through Your Name) 2005 PDF Yoga Mantra.pdf": "Numeros Vision Classical Sound and Name Compendium (NV-CSNC-43)",
    "Chaldean Numerology PDF Numbers Pythagoras.pdf": "Numeros Vision Chaldean Harmonic Compendium (NV-CHC-44)",
    "Chinese Numerology 1998 PDF.pdf": "Numeros Vision Classical Nine-Square Lo Shu System (NV-CNLS-45)",
    "Meaning and Magic of Numbers PDF Planets In Astrology Angel.pdf": "Numeros Vision Planetary and Number Symbolism Archive (NV-PNSA-46)",
    "Numerology The Magic of Numbers 1945 PDF Pi Numbers.pdf": "Numeros Vision Classical Numerology Manual (NV-CNM-47)",
    "Understanding Numerology Basics PDF.pdf": "Numeros Vision Foundational Vibrational Ledger (NV-FVL-48)",
    "Nadi Notes PDF Books Prediction.pdf": "Numeros Vision Classical Nadi Synthesis (NV-CNS-49)",
    "nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf": "Numeros Vision Classical Nadi Event System (NV-CNES-50)",
    "Nadi-Astrology-Marriage-And-Relationships.pdf": "Numeros Vision Relational Dynamics Canon (NV-RDC-51)",
}

DEFAULT_PROPRIETARY_NAME = "Numeros Vision Proprietary Knowledge Core (NV-KC-VAULT)"

# Patterns of authors, training files, or personal client identities to scrub
PII_AND_AUTHOR_PATTERNS = [
    # Astrology discipline names to pure numerology
    (re.compile(r'\b(Krishnamurti\s+Paddhati|KP(\s+Astrology)?)\b', re.IGNORECASE), "Dasha Timing"),
    (re.compile(r'\b(Bhrigu\s+Nandi\s+Nadi|BNN)\b', re.IGNORECASE), "Planetary Numerology"),
    (re.compile(r'\b(Lal\s+Kitab)\b', re.IGNORECASE), "Harmonic Elemental System"),
    (re.compile(r'\b(Vedic\s+Astrology|Parashari\s+Jyotish|Vedic\s+Jyotish)\b', re.IGNORECASE), "Vedic Numerology"),
    (re.compile(r'\b(Vedic\s+Kundli|Kundli|Kundali)\b', re.IGNORECASE), "Numerology Grid"),
    (re.compile(r'\b(ephemeris(\s+tables)?)\b', re.IGNORECASE), "cyclical calculation tables"),
    (re.compile(r'\b(deterministic\s+calculation\s+engine)\b', re.IGNORECASE), "classical calculation system"),
    (re.compile(r'\b(hard-?coded(\s+algorithms?)?)\b', re.IGNORECASE), "verified mathematical rules"),
    (re.compile(r'\b(hallucinat\w*)\b', re.IGNORECASE), "unverified claims"),
    (re.compile(r'\bCharm\s+AI\s+Oracle\b', re.IGNORECASE), "Charm AI"),
    (re.compile(r'\bAI\s+Oracle\b', re.IGNORECASE), "Charm AI"),

    # Personal client names
    (re.compile(r'\b(Bhaskr|Bhaskar)\s*(Singh)?\b', re.IGNORECASE), "Analyzed Subject"),
    (re.compile(r'\b(Ummika)\s*(Singh)?\b', re.IGNORECASE), "Analyzed Subject"),
    (re.compile(r'\b(Kaashvi)\s*(Singh)?\b', re.IGNORECASE), "Analyzed Subject"),
    (re.compile(r'\b(Ankur)\s*(Sachdeva)?\b', re.IGNORECASE), "Analyzed Subject"),
    (re.compile(r'\b(Shally)\s*(Sharma)?\b', re.IGNORECASE), "Analyzed Subject"),
    (re.compile(r'\b(Neeraj)\b', re.IGNORECASE), "Consulted Practitioner"),

    # Author names and external entities
    (re.compile(r'\bUmang\s*Taneja(\'s)?\b', re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r'\bTaneja(\'s)?\b', re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r'\bGautam\s*Verma(\'s)?\b', re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r'\bKpastrologer(\.co\.in)?\b', re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r'\bYoga\s*Mantra(\'s)?\b', re.IGNORECASE), "Classical Chaldean Tradition"),
    (re.compile(r'\b(Dr\.\s*)?Chaitanyaa?\s*Miss?ra(\'s)?\b', re.IGNORECASE), "Numeros Vision Classical Hermeneutics"),
    (re.compile(r'\bHarish\s*Johari(\'s)?\b', re.IGNORECASE), "Classical Ayurvedic Numerological Tradition"),
    (re.compile(r'\bVijaya\s*Kumar(\'s)?\b', re.IGNORECASE), "Classical Vedic Mathematical Tradition"),
    (re.compile(r'\bMari\s*Silva(\'s)?\b', re.IGNORECASE), "Classical Jyotish Principles"),
    (re.compile(r'\bCheiro\'s\s+Book\s+of\s+Numbers\b', re.IGNORECASE), "Numeros Vision Chaldean Harmonic Archive"),
    (re.compile(r'\bCheiro(\'s)?\b', re.IGNORECASE), "Classical Chaldean System"),
    (re.compile(r'\bTalking\s+Nummbers\b', re.IGNORECASE), "Numeros Vision Foundational Research"),
    (re.compile(r'\bLinda\s+Goodman(\'s)?\b', re.IGNORECASE), "Classical Astro-Numerology Canon"),
    (re.compile(r'\bMatthew\s+Oliver\s+Goodwin(\'s)?\b', re.IGNORECASE), "Classical Numerology System"),
    (re.compile(r'\bMatthew\s+Goodwin(\'s)?\b', re.IGNORECASE), "Classical Numerology System"),
    (re.compile(r'\bGoodwin\b', re.IGNORECASE), "Classical Numerology System"),
    (re.compile(r'\bHans\s+Decoz\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bDecoz\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bFaith\s+Javane\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bJavane\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bDusty\s+Bunker\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bBunker\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bFlorence\s+Campbell\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bRichard\s+Webster\b', re.IGNORECASE), "Classical Lo Shu Archive"),
    (re.compile(r'\bEric\s+Temple\s+Bell\b', re.IGNORECASE), "Classical Mathematical Archive"),
    (re.compile(r'\bE\.T\.\s+Bell\b', re.IGNORECASE), "Classical Mathematical Archive"),
    (re.compile(r'\bVincent\s+Lopez\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bMark\s+Crawford\b', re.IGNORECASE), "Classical Numerology Archive"),
    (re.compile(r'\bSepharial(\'s)?\b', re.IGNORECASE), "Classical Astro-Numerology Archive"),
    (re.compile(r'\bAccurate\s+Predictive\s+Methodology\b', re.IGNORECASE), "Numeros Vision Classical Nadi Event System"),
    (re.compile(r'\bFortune\s+Through\s+Your\s+Name\b', re.IGNORECASE), "Numeros Vision Classical Sound and Name Compendium"),
    (re.compile(r'\bMeaning\s+and\s+Magic\s+of\s+Numbers\b', re.IGNORECASE), "Numeros Vision Planetary and Number Symbolism Archive"),
    (re.compile(r'\bNumbers\s+Their\s+Meaning\s+and\s+Magic\b', re.IGNORECASE), "Numeros Vision Planetary and Number Symbolism Archive"),
    (re.compile(r'\bThe\s+Magic\s+of\s+Numbers\b', re.IGNORECASE), "Numeros Vision Classical Numerology Manual"),

    # File extensions and file references
    (re.compile(r'\s*\.(pdf|docx|xlsx|md|csv)\b', re.IGNORECASE), ""),
    (re.compile(r'\b(pdf|docx|xlsx)\b', re.IGNORECASE), "treatise"),

    # Personal emails and phone numbers
    (re.compile(r'[\w\.-]+@[\w\.-]+\.\w+', re.IGNORECASE), "[Protected Contact]"),
    (re.compile(r'\b\+?91[\-\s]?\d{10}\b|\b\d{10}\b'), "[Protected Identifier]"),
]

def mask_source_name(raw_source: str) -> str:
    """
    Guarantees that no raw filename, book title, or author name is ever returned.
    Maps to prestigious Numeros Vision Vault identities.
    """
    if not raw_source:
        return DEFAULT_PROPRIETARY_NAME

    clean_key = raw_source.strip()
    if clean_key.startswith("Numeros Vision"):
        return clean_key

    if clean_key in SOURCE_PROPRIETARY_MAPPING:
        return SOURCE_PROPRIETARY_MAPPING[clean_key]

    for k, v in SOURCE_PROPRIETARY_MAPPING.items():
        if k.lower() in clean_key.lower() or clean_key.lower() in k.lower():
            return v

    # Synthesis modules
    if "synthesis" in clean_key.lower():
        prefix = clean_key.replace(":", " ·").replace("", "-")
        return f"Numeros Vision Synthesis Core: {prefix}"

    # Fallback to deterministic hashed vault ID
    code = hashlib.md5(clean_key.encode('utf-8')).hexdigest()[:4].upper()
    return f"Numeros Vision Sovereign Archive (NV-VAULT-{code})"


def sanitize_location(raw_location: str) -> str:
    """
    Sanitizes location strings (e.g., 'Page 42', 'Table 3') into clean analytical nodes.
    Removes any embedded filenames or external links.
    """
    if not raw_location:
        return "Analytical Reference Node"

    clean = raw_location.strip()
    if clean.startswith("Section NV-SEC-") or clean.startswith("Matrix Index") or clean.startswith("Archival Node"):
        return clean

    clean = re.sub(r'[\w\-_\.]+\.(pdf|docx|xlsx|md)', '', clean, flags=re.IGNORECASE).strip()
    clean = re.sub(r'[\(\)]', '', clean).strip()

    # Convert Page X to Section NV-SEC-X
    m_page = re.search(r'Page\s*(\d+)', clean, re.IGNORECASE)
    if m_page:
        return f"Section NV-SEC-{m_page.group(1)}"

    # Convert Slide / Table
    m_table = re.search(r'(Table|Slide|Row)\s*(\d+)', clean, re.IGNORECASE)
    if m_table:
        return f"Matrix Index NV-{m_table.group(1).upper()}-{m_table.group(2)}"

    if clean:
        return f"Archival Node {clean[:30]}"
    return "Analytical Section Node"


def sanitize_text(text: str) -> str:
    """
    Removes private use area Unicode, control characters, author names,
    client names, file extensions, and phone numbers.
    """
    if not text:
        return ""

    # Strip Private Use Area unicode
    res = re.sub(r'[\ue000-\uf8ff\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)

    # Apply all PII and Author scrubbing rules
    for pat, repl in PII_AND_AUTHOR_PATTERNS:
        res = pat.sub(repl, res)

    return res


def sanitize_citation(citation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes a single citation dictionary before presentation or API response.
    """
    raw_source = citation.get("source", "")
    raw_location = citation.get("location", "")
    raw_excerpt = citation.get("excerpt", "") or citation.get("content", "")

    return {
        "source": mask_source_name(raw_source),
        "location": sanitize_location(raw_location),
        "category": citation.get("category", "Proprietary Classical Synthesis"),
        "excerpt": sanitize_text(raw_excerpt[:280]) + ("..." if len(raw_excerpt) > 280 else "")
    }


def sanitize_payload(payload: Any) -> Any:
    """
    Recursively inspects and sanitizes any dict or list payload to ensure zero leaks.
    """
    if isinstance(payload, dict):
        new_dict = {}
        for k, v in payload.items():
            if k == "grounded_citations" and isinstance(v, list):
                new_dict[k] = [sanitize_citation(item) if isinstance(item, dict) else item for item in v]
            elif k == "source" and isinstance(v, str):
                new_dict[k] = mask_source_name(v)
            elif k == "location" and isinstance(v, str):
                new_dict[k] = sanitize_location(v)
            elif k == "grounded_source" and isinstance(v, str):
                new_dict[k] = "Numeros Vision Proprietary Knowledge Core (NV-KC-VAULT)"
            elif isinstance(v, (dict, list)):
                new_dict[k] = sanitize_payload(v)
            elif isinstance(v, str):
                new_dict[k] = sanitize_text(v)
            else:
                new_dict[k] = v
        return new_dict
    elif isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    elif isinstance(payload, str):
        return sanitize_text(payload)
    return payload
