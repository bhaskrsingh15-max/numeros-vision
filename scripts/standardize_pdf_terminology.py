import os
import re

pdf_file = 'app/services/pdf_report_generator.py'

with open(pdf_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace "Chapter / Section" with "Section / Standard Topic"
text = text.replace('<b>Chapter / Section</b>', '<b>Section / Standard Topic</b>')
text = text.replace('ChapterH1', 'SectionH1')

# Replace "Chapter X:" with "Section X:"
text = re.sub(r'Chapter\s+(\d+):', r'Section \1:', text)
text = re.sub(r'Chapter\s+(\d+)\s*<', r'Section \1<', text)

# For Basic 3 pages:
text = text.replace('Section 1: Deterministic Calculations & Natal Grid', 'Personal Profile, Natal Lo Shu Grid & 8-Plane Elemental Audit')
text = text.replace('Section 2: Personal Destiny Blueprint', '8 Elemental Planes, Sovereign Raj Yogas & Remedial Blueprint')

# Save updated pdf generator
with open(pdf_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated app/services/pdf_report_generator.py to standard structured terminology!")
