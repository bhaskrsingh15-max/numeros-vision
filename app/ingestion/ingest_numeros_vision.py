"""
NUMEROS VISION — COMPREHENSIVE MULTI-SOURCE CORPUS INGESTION ENGINE
Ingests, cleans, chunks, and categorizes:
1. Classical Numerology & Master Guidebooks (Numeros Vision Classical Methodology, Classical Vedic Tradition, Vedic Mathematical Tradition, Cheiro, etc.)
2. Crystal & Gemstone Astrology Guides (360 Sabian Crystals, Planetary Frequency Attunement)
3. 25 All-In-One Astrological, Lal Kitab & Elemental Remedies Kits
4. Lo Shu Grid 8-Plane Analysis, Missing & Repeat Number Compendiums
5. Vastu Shastra & Space Energy Applications
6. Name Spelling Optimization, Baby Naming & Business Trademark Tools
7. Bhrigu Nandi Nadi (BNN) Planetary Combinations & Midas Touch Wealth Astrology
8. Real Client Full & Short Sample Reports (Bhaskr Singh, Ummika Singh, Kaashvi Singh, Ankur Sachdeva, Shally Sharma)
9. Preserves all previously ingested synthesis corpora with zero regression.
"""

import os
import glob
import json
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

import pypdf
import docx
import openpyxl

from app.engine.source_privacy_shield import (
    mask_source_name,
    sanitize_location,
    sanitize_text,
)

DOWNLOADS_DIR = r"C:\Users\Bhaskr Singh\Downloads"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "knowledge_base"
OUTPUT_FILE = OUTPUT_DIR / "numeros_vision_corpus.json"

# Master Registry of Verified Knowledge Sources
NUMEROS_VISION_FILES = [
    # ── Classical Numerology & Master Guidebooks ──
    "numerology Numeros Vision Classical Methodology .pdf",
    "Numerology by Numeros Vision Classical Methodology Welcome Kit.pdf",
    "The Ultimate Guide to Numerology Use_.(1).pdf",
    "Numerology (Classical Vedic Tradition) (Z-Library).pdf",
    "Numerology (Vedic Mathematical Tradition) (Z-Library).pdf",
    "Numerology the Complete Guide, Volume 1-The Personality Reading.pdf",
    "Professional Numerology notes.pdf",
    "Professional_Numerology_Notes_EDITABLE_TABLES.docx",
    "Numeros Vision Brand Blueprint.docx",
    "Cheiros_Book_of_Numbers_Study_Notes.docx",
    "NP-Karmic-Empowerment-With-Numerology_.pdf",
    "Basic Numerology Course - Talking Nummbers.pdf",
    "Basic Numerology Course - Talking Nummbers.hindi.pdf",
    "Mulank and Bhagyank Predictions Guide PDF Psychology Behavioural Sciences.pdf",
    "81 Driver-Conductor Combinations in Numerology PDF Planets In Astrology Wisdom.pdf",
    "Advanced_Numerology_Course_Guide___PDF___Devi___Prayer.pdf",
    "Advanced_Numerology_Study_Notes___PDF.pdf",
    "Traits and Insights of Numerology 1 PDF Leadership Physical Attractiveness.pdf",
    "Traits of Number 1 in Vedic Numerology PDF.pdf",
    "Understanding Mulank 1 in Numerology PDF Leadership Creativity.pdf",
    "Understanding Name Numbers in Numerology PDF Luck Planets.pdf",
    "Understanding Numerology Numbers 1-9 PDF.pdf",
    "Understanding_Compound_Numbers_in_Numerology___PDF___Luck.pdf",
    "Understanding_Name_Numerology_Numbers___PDF.pdf",
    "NumerologyRepetitiveNos1-9_updated.pdf",

    # ── Crystal & Gemstone Astrology ──
    "The_Complete_Guide_to_Crystal_Astrology_360_Crystals_and_Sabian.pdf",

    # ── All-In-One Astrological & Elemental Remedies ──
    "25 astrological remedies all in one  (1)_compressed.pdf",
    "25-Astrology-remedies-kit-io2rbv.pdf",
    "Numerology Insights and Remedies Report PDF Luck.pdf",

    # ── Lo Shu Grid & Planes ──
    "Lo Shu Grid Analysis and Remedies PDF Planets In Astrology Intuition.pdf",
    "Lo shu grid.pdf",

    # ── Vastu & Spatial Energy ──
    "Practical_Vaastu_Insights_and_Applications___PDF___Basement.pdf",
    "Vastu_Planning_and_Design_Steps___PDF.pdf",

    # ── Naming, Brand & Baby Naming ──
    "Name Spelling Correction Insights PDF Language Arts & Discipline.pdf",
    "Chaldean Numerology Name Analysis PDF Sports & Recreation Wellness.pdf",
    "BabyNamingNumerology_2026-09-08.pdf",
    "BUSINESS NAME GENERATOR TOOL.docx",
    "BRAND NAME -PROMPT.docx",

    # ── Mobile, Asset & Vehicle Numerology ──
    "Vehicle Number Luck Analysis PDF.pdf",
    "Mobile_Numerology_Master_Sheet___PDF___Marriage.pdf",
    "Numerology-Based_Mobile_Wallpapers___PDF.pdf",

    # ── Planetary, BNN & Wealth Astrology ──
    "THE BOOK OF NAKSHATRAS.pdf",
    "Vedic Astrology (Classical Astrological Framework) .pdf",
    "Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise.md",
    "Midas_Touch_Astrology_of_Wealth_Markdown_Study_Edition.md",
    "Planet details in depth.pdf",
    "Profession, Business, and Education Mastery Class 10 _ PDF _ Planets In Astrology _ Hindu Astrology.pdf",
    "Calculating Mahadasha in Vedic Astrology PDF Planets In Astrology Self-Improvement.pdf",
    "RIL_2025_Validated_Numerology_Output.xlsx",

    # ── Real Client Sample Reports (Style, Diagnostic Tone, and Prescription Architecture) ──
    "Bhaskr_Singh_numerology.pdf",
    "Bhaskr_Singh_short_report.pdf",
    "Ummika_Singh_numerology.pdf",
    "Ummika_Singh_short_report.pdf",
    "Kaashvi_Singh_numerology.pdf",
    "Kaashvi_Singh_short_report.pdf",
    "Ankur_Sachdeva__numerology.pdf",
    "Ankur_Sachdeva_short_report.pdf",
    "Shally_Sharma_short_report.pdf",
    "serve-me-my-success-bhaskr singh-28-11-1981.pdf",
    "ummika-singh_name_balancing_report_2026-09-08.pdf"
]

def classify_category(filename: str) -> str:
    fn = filename.lower()
    if any(k in fn for k in ["bhaskr", "ummika", "kaashvi", "ankur", "shally", "neeraj", "serve-me-my-success", "short_report"]):
        return "sample_client_report"
    elif "crystal" in fn:
        return "crystal_gemstone_guide"
    elif "remed" in fn:
        return "remedies_compendium"
    elif "lo shu" in fn or "lo_shu" in fn:
        return "lo_shu_guide"
    elif "vastu" in fn or "vaastu" in fn:
        return "vastu_handbook"
    elif any(k in fn for k in ["name", "naming", "brand"]):
        return "naming_guide"
    elif any(k in fn for k in ["bhrigu", "nakshatra", "midas", "vedic astrology", "mahadasha", "profession"]):
        return "astrology_bnn_treatise"
    elif any(k in fn for k in ["vehicle", "mobile"]):
        return "asset_numerology_guide"
    return "authoritative_numerology_book"


def clean_chunk(text: str) -> str:
    # Collapse multiple spaces and line breaks while preserving punctuation and scrubbing PII
    text = re.sub(r'[\r\t]', ' ', text)
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    return sanitize_text(text.strip())


def chunk_text(text: str, max_chars: int = 650, min_chars: int = 40) -> List[str]:
    """Splits dense document text into semantically cohesive passages."""
    paragraphs = re.split(r'\n\s*\n|\n(?=[A-Z0-9\-\✦\•])', text)
    chunks = []
    current = ""
    for p in paragraphs:
        p_clean = clean_chunk(p)
        if not p_clean or len(p_clean) < min_chars:
            continue
        if len(current) + len(p_clean) < max_chars:
            current += ("\n" + p_clean if current else p_clean)
        else:
            if current:
                chunks.append(current)
            current = p_clean
    if current and len(current) >= min_chars:
        chunks.append(current)
    return chunks


def parse_pdf(file_path: str, category: str) -> List[Dict[str, Any]]:
    passages = []
    try:
        reader = pypdf.PdfReader(file_path)
        source_name = mask_source_name(os.path.basename(file_path))
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue
            page_chunks = chunk_text(text)
            for idx, chunk in enumerate(page_chunks, start=1):
                passages.append({
                    "source": source_name,
                    "location": sanitize_location(f"Page {page_num}, Section {idx}"),
                    "category": category,
                    "provenance": "verified_numeros_vision",
                    "content": sanitize_text(chunk)
                })
    except Exception as e:
        print(f"  [ERROR] reading PDF {file_path}: {e}")
    return passages


def parse_docx(file_path: str, category: str) -> List[Dict[str, Any]]:
    passages = []
    try:
        doc = docx.Document(file_path)
        source_name = mask_source_name(os.path.basename(file_path))
        full_text = []
        for p in doc.paragraphs:
            if p.text and p.text.strip():
                full_text.append(p.text.strip())
        for t_idx, table in enumerate(doc.tables, start=1):
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells if c.text.strip()]
                if cells:
                    full_text.append(" | ".join(cells))
        
        blob = "\n\n".join(full_text)
        chunks = chunk_text(blob, max_chars=700)
        for idx, chunk in enumerate(chunks, start=1):
            passages.append({
                "source": source_name,
                "location": sanitize_location(f"Section {idx}"),
                "category": category,
                "provenance": "verified_numeros_vision",
                "content": sanitize_text(chunk)
            })
    except Exception as e:
        print(f"  [ERROR] reading DOCX {file_path}: {e}")
    return passages


def parse_md(file_path: str, category: str) -> List[Dict[str, Any]]:
    passages = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as fh:
            text = fh.read()
        source_name = mask_source_name(os.path.basename(file_path))
        chunks = chunk_text(text, max_chars=700)
        for idx, chunk in enumerate(chunks, start=1):
            passages.append({
                "source": source_name,
                "location": sanitize_location(f"Section {idx}"),
                "category": category,
                "provenance": "verified_numeros_vision",
                "content": sanitize_text(chunk)
            })
    except Exception as e:
        print(f"  [ERROR] reading MD {file_path}: {e}")
    return passages


def parse_xlsx(file_path: str, category: str) -> List[Dict[str, Any]]:
    passages = []
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
        source_name = mask_source_name(os.path.basename(file_path))
        for sheetname in wb.sheetnames:
            sheet = wb[sheetname]
            sheet_rows = []
            for row in sheet.iter_rows(values_only=True):
                non_empty = [str(val).strip() for val in row if val is not None and str(val).strip() != '']
                if non_empty:
                    sheet_rows.append(" | ".join(non_empty))
            if sheet_rows:
                chunk = f"Sheet: {sheetname}\n" + "\n".join(sheet_rows)
                passages.append({
                    "source": source_name,
                    "location": sanitize_location(f"Sheet {sheetname}"),
                    "category": category,
                    "provenance": "verified_numeros_vision",
                    "content": sanitize_text(chunk)
                })
    except Exception as e:
        print(f"  [ERROR] reading XLSX {file_path}: {e}")
    return passages


def run_ingestion():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load existing corpus to preserve historical synthesis
    existing_passages = []
    existing_hashes = set()
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing_passages = data.get("passages", [])
                for p in existing_passages:
                    h = hashlib.sha256(p.get("content", "").strip().encode('utf-8')).hexdigest()
                    existing_hashes.add(h)
            print(f"Loaded {len(existing_passages)} existing passages from {OUTPUT_FILE}")
        except Exception as e:
            print(f"Notice: Failed to load previous corpus: {e}")

    newly_added = []
    processed_sources = set()

    print(f"\nStarting multi-source ingestion from {DOWNLOADS_DIR}...")

    for filename in NUMEROS_VISION_FILES:
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        if not os.path.exists(filepath):
            matches = glob.glob(os.path.join(DOWNLOADS_DIR, f"*{filename[:15]}*"))
            if matches:
                filepath = matches[0]
            else:
                print(f"  [SKIP] File not found: {filename}")
                continue

        base_name = os.path.basename(filepath)
        category = classify_category(base_name)
        print(f"Processing [{category}]: {base_name}")
        
        extracted = []
        if filepath.endswith('.pdf'):
            extracted = parse_pdf(filepath, category)
        elif filepath.endswith('.docx'):
            extracted = parse_docx(filepath, category)
        elif filepath.endswith('.md'):
            extracted = parse_md(filepath, category)
        elif filepath.endswith('.xlsx'):
            extracted = parse_xlsx(filepath, category)

        added_from_file = 0
        for p in extracted:
            h = hashlib.sha256(p["content"].strip().encode('utf-8')).hexdigest()
            if h not in existing_hashes:
                existing_hashes.add(h)
                newly_added.append(p)
                added_from_file += 1

        processed_sources.add(base_name)
        print(f"  -> Extracted {len(extracted)} passages ({added_from_file} new unique added).")

    # Combine existing and new passages
    final_passages = existing_passages + newly_added
    all_sources = sorted(list(set(p.get("source", "Unknown") for p in final_passages)))

    print("\n" + "=" * 70)
    print(f"INGESTION SUMMARY:")
    print(f"  - Prior Passages Preserved: {len(existing_passages)}")
    print(f"  - New Passages Added:       {len(newly_added)}")
    print(f"  - Total Corpus Passages:    {len(final_passages)}")
    print(f"  - Total Unique Sources:     {len(all_sources)}")
    print("=" * 70)

    # Save to disk
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "total_passages": len(final_passages),
            "sources_count": len(all_sources),
            "sources": all_sources,
            "passages": final_passages
        }, f, indent=2, ensure_ascii=False)

    print(f"Updated knowledge base successfully written to: {OUTPUT_FILE}\n")


if __name__ == "__main__":
    run_ingestion()
