import re

print("--- 1. Updating app/static/sample.html ---")
with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Format 1 renderLoShuCell missing branch
old_f1_gap = '''        if (cnt === 0) {
          return `
            <td style="border:1.5px dashed rgba(201,162,39,0.35); background:rgba(255,253,247,0.7); vertical-align:middle; text-align:center; padding:5px 3px; border-radius:4px;">
              <div style="font-size:9px; color:#A13030; font-weight:800; letter-spacing:0.04em;">[GAP]</div>
              <div style="font-size:11px; font-weight:700; color:#8C827A;">${num}${markerStr}</div>
              <div style="font-size:8px; color:#7A654D;">${label}</div>
            </td>
          `;
        }'''

new_f1_gap = '''        if (cnt === 0) {
          return `
            <td onclick="showPaywallUnlockModal('brief')" style="cursor:pointer; border:1.5px dashed rgba(201,162,39,0.55); background:linear-gradient(135deg, rgba(255,253,247,0.95), rgba(247,243,234,0.92)); vertical-align:middle; text-align:center; padding:4px 2px; border-radius:4px; transition:all 0.2s;" title="Click to Anveil Charm for Number ${num}">
              <div style="font-size:7.5px; color:#8B6914; font-weight:800; letter-spacing:0.03em;">🔒 ANVEIL CHARM</div>
              <div style="font-size:11px; font-weight:800; color:#523E28;">${num}${markerStr}</div>
              <div style="font-size:7.5px; color:#7A654D;">${label}</div>
            </td>
          `;
        }'''

if old_f1_gap in html:
    html = html.replace(old_f1_gap, new_f1_gap)
    print("Format 1 renderLoShuCell updated to Curiosity Lock!")
else:
    print("WARNING: old_f1_gap not found")

# Replace Format 3 renderLoShuCell missing branch
old_f3_gap = '''        if (cnt === 0) {
          return `
            <td style="border:1.5px dashed rgba(201,162,39,0.35); background:rgba(255,253,247,0.7); vertical-align:middle; text-align:center; padding:5px 3px; border-radius:4px;">
              <div style="font-size:9px; color:#A13030; font-weight:800; letter-spacing:0.04em;">[GAP]</div>
              <div style="font-size:11px; font-weight:700; color:#8C827A;">${num}${markerStr}</div>
              <div style="font-size:8px; color:#7A654D;">${label}</div>
            </td>
          `;
        }'''

# Replace summary below grid
old_summary_gap = '''                  <div><strong>Present:</strong> <span style="color:#16835B; font-weight:700;">${present.join(', ')} ✔</span></div>
                  <div><strong>Missing [GAP]:</strong> <span style="color:#A13030; font-weight:700;">${missing.join(', ')}</span></div>'''

new_summary_gap = '''                  <div><strong>Present Active:</strong> <span style="color:#16835B; font-weight:700;">${present.join(', ')} ✔</span></div>
                  <div><strong>🔒 Sleeping Charms (Voids):</strong> <span onclick="showPaywallUnlockModal('brief')" style="cursor:pointer; color:#8B6914; font-weight:800; text-decoration:underline;">${missing.map(m => `🔒 ${m}`).join(' ')} · Anveil to Unlock →</span></div>'''

if old_summary_gap in html:
    html = html.replace(old_summary_gap, new_summary_gap)
    print("Summary below Lo Shu grid updated with Sleeping Charms!")
else:
    print("WARNING: old_summary_gap not found")

old_f3_summary_gap = '<div><strong>Missing Digits [GAP]:</strong> <span style="color:#A13030;font-weight:700;">${missing.join(\', \')}</span></div>'
new_f3_summary_gap = '<div><strong>🔒 Sleeping Charms (To Anveil):</strong> <span style="color:#8B6914;font-weight:800;">${missing.map(m => `🔒 ${m}`).join(\', \')} (Anveil to Unlock)</span></div>'

if old_f3_summary_gap in html:
    html = html.replace(old_f3_summary_gap, new_f3_summary_gap)
    print("Format 3 summary updated with Sleeping Charms!")
else:
    print("WARNING: old_f3_summary_gap not found")

# Replace any second occurrence of old_f1_gap (Format 3)
if old_f1_gap in html:
    html = html.replace(old_f1_gap, new_f1_gap)
    print("Format 3 renderLoShuCell updated to Curiosity Lock!")

with open('app/static/sample.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved app/static/sample.html!")

print("\n--- 2. Updating app/services/pdf_report_generator.py ---")
with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    pdf_code = f.read()

old_pdf_cell = """            else:
                return Paragraph(f"<font size=10 color='#B33A3A'><b>{num}</b></font><br/><font size=7 color='#B33A3A'><b>Karmic Gap</b></font><br/><font size=7 color='#7A654D'>{elem}</font>", s['TableCellCenter'])"""

new_pdf_cell = """            else:
                return Paragraph(f"<font size=8 color='#8B6914'><b>🔒 ANVEIL CHARM</b></font><br/><font size=10 color='#523E28'><b>{num}</b></font><br/><font size=7 color='#7A654D'>{elem} · Unsealed</font>", s['TableCellCenter'])"""

if old_pdf_cell in pdf_code:
    pdf_code = pdf_code.replace(old_pdf_cell, new_pdf_cell)
    print("Lo Shu cell in pdf_report_generator.py updated to Curiosity Lock!")
else:
    print("WARNING: old_pdf_cell not found in pdf_report_generator.py")

pdf_code = pdf_code.replace("paired with 5 karmic gaps that indicate", "paired with 5 unsealed sleeping charms that indicate")

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(pdf_code)
print("Saved app/services/pdf_report_generator.py!")
