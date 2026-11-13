import json
import csv

inv = json.load(open('data/knowledge_base/FULL_RECONCILED_INVENTORY.json', encoding='utf-8'))

out_csv = 'docs/knowledge_audit/SOURCE_INVENTORY_MASTER.csv'

fields = [
    'source_id',
    'canonical_title',
    'original_filename',
    'group',
    'document_type',
    'size_bytes',
    'page_count',
    'extractable',
    'sha256',
    'duplicate_of',
    'rights_status',
    'ingestion_status',
    'notes'
]

rows = []

for item in inv:
    fn = item['filename']
    grp = item['group']
    sz = item['size_bytes']
    pg = str(item['pages'])
    ext = item['extractable']
    sha = item['sha256']
    
    # Determine canonical metadata
    doc_type = 'pdf_book'
    rights = 'pending_review'
    ingest = 'DISCOVERED'
    dup = 'NONE'
    notes = ''
    sid = 'SRC-' + sha[:8].upper()

    if fn == 'Nadi Notes PDF Books Prediction.pdf':
        sid = 'SRC-NADI-NOTES-2026'
        title = 'Nadi Notes: Compiled Multi-Branch Nadi & BNN Analysis (82 pp)'
        doc_type = 'secondary_analysis'
        rights = 'approved_internal_research'
        notes = 'Primary secondary analysis source; covers BNN karaka field, Bhrigu Prashna 107 lookup, 100 Nadi Sutras'
    elif 'accurate-predictive-methodology' in fn:
        sid = 'SRC-NADI-Classical Nadi-2013'
        title = 'Numeros Vision Classical Nadi Event System (Classical Nadi Tradition 2013)'
        doc_type = 'primary_book'
        notes = 'Comprehensive 277-page text on KP-Nadi sub-lord event combinations'
    elif fn == 'Nadi Astrolology Combiations.pdf':
        sid = 'SRC-NADI-VERMA-SHEET'
        title = 'Nadi Astrology Combinations Reference Sheet (Classical Nadi Tradition)'
        doc_type = 'reference_sheet'
        notes = '3-page compact event and profession combination summary'
    elif 'Classical Nadi Tradition - PDF - Astrological' in fn:
        sid = 'SRC-NADI-Classical Nadi-EXTRACT'
        title = 'Nadi Astrology by Classical Nadi Tradition (Extract / Preview)'
        doc_type = 'book_extract'
        notes = '36-page preview/extract of Classical Nadi Nadi doctrine'
    elif 'Bhrigu Nandi Nadi Astrology Basics' in fn:
        sid = 'SRC-BNN-BASICS'
        title = 'Bhrigu Nandi Nadi Astrology Basics'
        doc_type = 'course_notes'
        notes = '19-page primer on BNN karakatwas and planetary rules'
    elif 'Bhrigu Nandi Nadi Astrology Overview' in fn:
        sid = 'SRC-BNN-OVERVIEW'
        title = 'Bhrigu Nandi Nadi Astrology Overview'
        doc_type = 'course_notes'
        notes = '45-page overview of planetary combinations in BNN'
    elif 'Bhrigu Nandi Nadi Prediction Techniques' in fn:
        sid = 'SRC-BNN-PRED-TECH'
        title = 'Bhrigu Nandi Nadi Prediction Techniques'
        doc_type = 'course_notes'
        notes = '19-page guide to transit rounds and prediction'
    elif 'Bhrigu Nadi Astrology Insights _ PDF' in fn:
        sid = 'SRC-BNN-INSIGHTS-SCAN'
        title = 'Bhrigu Nadi Astrology Insights (Scanned 95 pp)'
        doc_type = 'scanned_book'
        notes = 'Scanned 95-page volume; transcribed into markdown'
    elif 'Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise' in fn:
        sid = 'SRC-BNN-INSIGHTS-TRANSCRIPT'
        title = 'Bhrigu Nadi Astrology Insights Complete Pagewise Markdown'
        doc_type = 'transcript'
        notes = 'Complete verified pagewise markdown transcription of 95-page scan'
    elif fn.startswith('Classical Nine-Square Lo Shu System PDF (1)'):
        sid = 'B3-DUP'
        title = 'Chinese Numerology (1998 Duplicate)'
        dup = 'B3'
        notes = 'Bit-identical copy of B3'
    elif fn.startswith('Classical Nine-Square Lo Shu System'):
        sid = 'B3'
        title = 'Numeros Vision Classical Nine-Square Lo Shu System (1998)'
        notes = 'Chinese 3x3 Lo Shu grid reference; scanned image PDF'
    elif fn.startswith('Planetary and Number Symbolism Archive') and '(1)' in fn:
        sid = 'B4-DUP'
        title = 'Numeros Vision Planetary and Number Symbolism Archive (Duplicate)'
        dup = 'B4'
        notes = 'Bit-identical copy of B4'
    elif fn.startswith('Planetary and Number Symbolism Archive'):
        sid = 'B4'
        title = 'Numeros Vision Planetary and Number Symbolism Archive'
        notes = 'Historical esoteric symbolism; scanned image PDF'
    elif fn.startswith('Numeros Vision Classical Numerology Manual 1945') and '(1)' in fn:
        sid = 'B5-DUP'
        title = 'Numeros Vision Classical Numerology Manual 1945 (Duplicate)'
        dup = 'B5'
        notes = 'Bit-identical copy of B5'
    elif fn.startswith('Numeros Vision Classical Numerology Manual 1945'):
        sid = 'B5'
        title = 'Numeros Vision Classical Numerology Manual (1945 Edition)'
        notes = '1945 historic volume; scanned image PDF'
    elif fn.startswith('Understanding Numerology Basics') and '(1)' in fn:
        sid = 'B6-DUP'
        title = 'Understanding Numerology Basics (Duplicate)'
        dup = 'B6'
        notes = 'Bit-identical copy of B6'
    elif fn.startswith('Understanding Numerology Basics'):
        sid = 'B6'
        title = 'Understanding Numerology: The Power to Know Anybody'
        notes = 'Modern general numerology primer; scanned image PDF'
    elif fn.startswith('You and Your Name'):
        sid = 'B1'
        title = 'Numeros Vision Classical Sound and Name Compendium (2005)'
        notes = 'Chaldean sound/vibration rationale; scanned image PDF'
    elif fn.startswith('Chaldean Numerology PDF Numbers Pythagoras'):
        sid = 'B2'
        title = 'Chaldean Numerology: Structured Learning Reference'
        notes = '133-page digital text layer with 31-section Table of Contents'
    else:
        title = fn.replace('.pdf', '').replace('_', ' ')

    rows.append({
        'source_id': sid,
        'canonical_title': title,
        'original_filename': fn,
        'group': grp,
        'document_type': doc_type,
        'size_bytes': sz,
        'page_count': pg,
        'extractable': ext,
        'sha256': sha,
        'duplicate_of': dup,
        'rights_status': rights,
        'ingestion_status': ingest,
        'notes': notes
    })

with open(out_csv, 'w', encoding='utf-8', newline='') as fp:
    writer = csv.DictWriter(fp, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {out_csv} with {len(rows)} entries.")
