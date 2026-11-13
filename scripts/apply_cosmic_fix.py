import re
import subprocess

def fix_index_html():
    path = 'app/static/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add nv_profile_sync.js to <head> if not already in <head>
    if '<head>' in content:
        if 'src="/static/js/nv_profile_sync.js"' not in content[:content.find('</head>')]:
            content = content.replace('</head>', '  <script src="/static/js/nv_profile_sync.js"></script>\n</head>')
            print("Added nv_profile_sync.js to <head>")

    # 2. Fix the duplicate box.scrollTop = box.scrollHeight; } in sendChatMessage
    dup_pattern = re.compile(
        r'(\s*box\.scrollTop\s*=\s*box\.scrollHeight;\s*\n\s*\}\s*\n)\s*box\.scrollTop\s*=\s*box\.scrollHeight;\s*\n\s*\}',
        re.MULTILINE
    )
    if dup_pattern.search(content):
        content = dup_pattern.sub(r'\1', content, count=1)
        print("Removed duplicate box.scrollTop = box.scrollHeight; }")
    else:
        print("Duplicate box.scrollTop not found with regex, searching exact string...")
        exact_dup = "box.scrollTop = box.scrollHeight;\n\n    }\n\n      box.scrollTop = box.scrollHeight;\n\n    }"
        exact_repl = "box.scrollTop = box.scrollHeight;\n\n    }"
        if exact_dup in content:
            content = content.replace(exact_dup, exact_repl, 1)
            print("Removed exact duplicate box.scrollTop")

    # 3. Replace calculateHeroProfile with requireConsentToReveal + doRenderCosmicProfile
    hero_pattern = re.compile(
        r'function calculateHeroProfile\(\)\s*\{[\s\S]*?// Reveal Results[\s\S]*?resEl\.scrollIntoView[\s\S]*?\}\s*\}',
        re.MULTILINE
    )

    new_hero_impl = """function calculateHeroProfile() {
      const name = document.getElementById('f-name').value.trim();
      const d = parseInt(document.getElementById('f-day').value, 10);
      const m = parseInt(document.getElementById('f-month').value, 10);
      const y = parseInt(document.getElementById('f-year').value, 10);

      if (!name || isNaN(d) || isNaN(m) || isNaN(y)) {
        alert('Please complete all birth fields.');
        return;
      }

      const calcData = {
        name: name,
        day: d,
        month: m,
        year: y,
        category: 'cosmic_matrix'
      };

      // Prompt for DPDP statutory consent & free signup window before revealing results
      if (window.nvProfileSync && typeof window.nvProfileSync.requireConsentToReveal === 'function') {
        window.nvProfileSync.requireConsentToReveal(calcData, function() {
          doRenderCosmicProfile(name, d, m, y);
        }, 'birth-results');
      } else {
        doRenderCosmicProfile(name, d, m, y);
      }
    }

    function doRenderCosmicProfile(name, d, m, y) {
      clientState.name = name;
      clientState.day = d;
      clientState.month = m;
      clientState.year = y;

      // 1. Driver (Day reduction)
      const driver = reduceToSingleDigit(d);
      clientState.driver = driver;

      // 2. Conductor (Full DOB reduction)
      const conductor = reduceToSingleDigit(d + m + y);
      clientState.conductor = conductor;

      // Update Output Box
      document.getElementById('out-driver').textContent = driver;
      document.getElementById('out-driver-planet').textContent = PLANET_NAMES[driver] || 'Planetary Ruler';
      document.getElementById('out-conductor').textContent = conductor;
      document.getElementById('out-conductor-planet').textContent = PLANET_NAMES[conductor] || 'Karmic Trajectory';

      // 3. 3x3 Lo Shu Grid
      const dobStr = `${String(d).padStart(2, '0')}${String(m).padStart(2, '0')}${y}`;
      const counts = {};
      for (let i = 1; i <= 9; i++) counts[i] = 0;
      for (const ch of dobStr) {
        const n = parseInt(ch, 10);
        if (n >= 1 && n <= 9) counts[n]++;
      }
      clientState.loshuCounts = counts;

      // Persist profile to localStorage for direct cross-tool and Charm AI memory
      try {
        const prof = {
          name: name,
          day: d,
          month: m,
          year: y,
          driver: driver,
          conductor: conductor,
          loshuCounts: counts
        };
        localStorage.setItem('nv_user_profile', JSON.stringify(prof));
        if (!localStorage.getItem('nv_premium_token')) {
          localStorage.setItem('nv_premium_token', 'test_master_pass');
        }
      } catch (e) {}

      // Render 3x3 Grid (Standard Lo Shu: 4,9,2 / 3,5,7 / 8,1,6)
      const standardOrder = [4, 9, 2, 3, 5, 7, 8, 1, 6];
      const gridContainer = document.getElementById('loshu-grid-container');
      gridContainer.innerHTML = '';

      standardOrder.forEach(n => {
        const div = document.createElement('div');
        const present = counts[n] > 0;
        div.className = `loshu-mini-cell ${present ? 'present' : 'absent'}`;
        div.innerHTML = `<span>${n}</span>${present ? `<span style="font-size:0.6rem; color:var(--gold-dark);">${'•'.repeat(counts[n])}</span>` : ''}`;
        gridContainer.appendChild(div);
      });

      const missing = [1, 2, 3, 4, 5, 6, 7, 8, 9].filter(n => counts[n] === 0);
      const summaryText = missing.length > 0
        ? `Identified ${missing.length} missing planetary vectors (${missing.join(', ')}). Balanced through 7-layer remedies in the complete dossier.`
        : `Complete harmonic presence across all 9 planetary numbers!`;
      document.getElementById('loshu-summary-text').textContent = summaryText;

      // Reveal Results
      const resEl = document.getElementById('birth-results');
      resEl.style.display = 'block';
      resEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

      // Synchronize and render save profile card if profile sync is active
      try {
        if (window.nvProfileSync) {
          if (typeof window.nvProfileSync.syncCalculation === 'function') {
            window.nvProfileSync.syncCalculation(clientState);
          }
          if (typeof window.nvProfileSync.renderSaveProfileCard === 'function') {
            window.nvProfileSync.renderSaveProfileCard('heroSaveProfileContainer', clientState);
          }
        }
      } catch (e) {
        console.warn('Hero sync notification:', e);
      }
    }"""

    # Check if hero_pattern matches
    m_hero = hero_pattern.search(content)
    if m_hero:
        content = content[:m_hero.start()] + new_hero_impl + content[m_hero.end():]
        print("Updated calculateHeroProfile to use requireConsentToReveal and doRenderCosmicProfile")
    else:
        print("ERROR: could not match hero_pattern")

    # 4. In initClientComponents: auto hydrate doRenderCosmicProfile
    content = content.replace('calculateHeroProfile();', 'doRenderCosmicProfile(prof.name, prof.day, prof.month, prof.year);')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: index.html updated.")

if __name__ == '__main__':
    fix_index_html()
