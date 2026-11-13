with open('app/static/year_2027.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    <!-- SAMPLE PREVIEWS -->
    <div class="sample-download-card" id="sample-preview">
      <h3 style="margin-bottom:8px;">Inspect 24-Page Sample Dossiers</h3>
      <p style="color:var(--ink-muted); margin-bottom:20px; font-size:0.95rem;">Review the layout, typography, and mathematical rigor before ordering your personal copy.</p>
      <div style="display:flex; flex-wrap:wrap; gap:18px; justify-content:center;">
        <div class="sample-badge-item" style="display:inline-flex; flex-direction:column; align-items:center; gap:8px;">
          <span style="font-weight:600; font-size:0.95rem; color:var(--ink-dark);">Sample A: Arun Sharma (Mulank 1, Bhagyank 4, Personal Year 5)</span>
          <button type="button" class="btn-outline" disabled style="opacity:0.75; cursor:not-allowed; font-size:0.9rem; padding:10px 20px;">Sample preview coming soon</button>
        </div>
        <div class="sample-badge-item" style="display:inline-flex; flex-direction:column; align-items:center; gap:8px;">
          <span style="font-weight:600; font-size:0.95rem; color:var(--ink-dark);">Sample B: Anil Kumar (Mulank 1, Bhagyank 1, Personal Year 8)</span>
          <button type="button" class="btn-outline" disabled style="opacity:0.75; cursor:not-allowed; font-size:0.9rem; padding:10px 20px;">Sample preview coming soon</button>
        </div>
      </div>
    </div>'''

replacement = '''    <!-- SAMPLE PREVIEWS -->
    <div class="sample-download-card" id="sample-preview">
      <h3 style="margin-bottom:8px;">Inspect 24-Page Sample Dossiers</h3>
      <p style="color:var(--ink-muted); margin-bottom:20px; font-size:0.95rem;">Review the layout, typography, and mathematical rigor before ordering your personal copy.</p>
      <div style="display:flex; flex-wrap:wrap; gap:20px; justify-content:center;">
        <div class="sample-badge-item" style="display:inline-flex; flex-direction:column; align-items:center; gap:8px; max-width:340px; text-align:center;">
          <span style="font-weight:600; font-size:0.95rem; color:var(--ink-dark);">Sample A: Arun Sharma (Mulank 1, Bhagyank 4, Personal Year 5)</span>
          <a href="/samples/sample_arun_sharma_2027.pdf" target="_blank" download class="btn-outline" style="font-size:0.9rem; padding:10px 20px; text-decoration:none;">Download Sample A (PDF)</a>
          <span style="font-family:monospace; font-size:0.70rem; color:var(--ink-muted); word-break:break-all;">SHA-256: 41f480f4975aa5518a5d744b08bee3741f06516d95dc8f266c8db2ef70a24d35</span>
        </div>
        <div class="sample-badge-item" style="display:inline-flex; flex-direction:column; align-items:center; gap:8px; max-width:340px; text-align:center;">
          <span style="font-weight:600; font-size:0.95rem; color:var(--ink-dark);">Sample B: Anil Kumar (Mulank 1, Bhagyank 1, Personal Year 8)</span>
          <a href="/samples/sample_anil_kumar_2027.pdf" target="_blank" download class="btn-outline" style="font-size:0.9rem; padding:10px 20px; text-decoration:none;">Download Sample B (PDF)</a>
          <span style="font-family:monospace; font-size:0.70rem; color:var(--ink-muted); word-break:break-all;">SHA-256: b514a091e01406f1449f9472404c1f70351c8341a1101fbc07a817e68e192e4d</span>
        </div>
      </div>
    </div>'''

text_norm = text.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
replacement_norm = replacement.replace('\r\n', '\n')

assert target_norm in text_norm, 'Target not found in year_2027.html'
new_text = text_norm.replace(target_norm, replacement_norm)

with open('app/static/year_2027.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(new_text)

print('Updated sample preview block in year_2027.html successfully!')
