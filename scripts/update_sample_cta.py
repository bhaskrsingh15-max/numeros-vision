import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                <div style="border-top:1px dashed rgba(201,162,39,0.3); padding-top:4px; font-size:9px; color:#523E28; line-height:1.45;">
                  <div style="margin-bottom:2px;">
                    <strong style="color:#16835B;">🔓 Know Present Numbers:</strong> 
                    <span onclick="showPaywallUnlockModal('master')" style="cursor:pointer; color:#16835B; font-weight:800; text-decoration:underline;">[ ${present.join(', ')} ] Harmonize Overdrive (@ ₹510) →</span>
                  </div>
                  <div>
                    <strong style="color:#8B6914;">🔒 Full Anveil Charm (Missing):</strong> 
                    <span onclick="showPaywallUnlockModal('roadmap')" style="cursor:pointer; color:#8B6914; font-weight:800; text-decoration:underline;">[ ${missing.join(', ')} ] Name Balancing &amp; Vastu (@ ₹1,050) →</span>
                  </div>
                  <div style="font-size:8px; color:#7A654D; margin-top:2px;">${freqSummary}</div>
                </div>"""

replacement = """                <div style="border-top:1px dashed rgba(201,162,39,0.3); padding-top:6px; font-size:9px; color:#523E28; line-height:1.45;">
                  <div style="margin-bottom:4px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:4px;">
                    <span onclick="showPaywallUnlockModal('master')" style="cursor:pointer; display:inline-flex; align-items:center; gap:4px; background:rgba(22,131,91,0.08); border:1px solid #16835B; padding:3.5px 7px; border-radius:4px; color:#16835B; font-weight:800; font-size:9.5px; text-decoration:none;">
                      🔓 Active Charm Present @ 510 [ ${present.join(', ')} ] →
                    </span>
                    <span onclick="showPaywallUnlockModal('roadmap')" style="cursor:pointer; display:inline-flex; align-items:center; gap:4px; background:rgba(201,162,39,0.12); border:1px solid #8B6914; padding:3.5px 7px; border-radius:4px; color:#8B6914; font-weight:800; font-size:9.5px; text-decoration:none;">
                      🔒 Anveil Charm Missing @ 1050 [ ${missing.join(', ')} ] →
                    </span>
                  </div>
                  <div style="font-size:8px; color:#7A654D; margin-top:2px;">${freqSummary} · Tap any cell or CTA to inspect tailored dossier</div>
                </div>"""

if target in text:
    text = text.replace(target, replacement, 1)
    with open('app/static/sample.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: sample.html updated!")
else:
    print("WARNING: target not found in sample.html")
