import re

def update_index_html():
    path = 'app/static/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Static options for f-day
    day_options = ['<option value="">DD</option>']
    for d in range(1, 32):
        day_options.append(f'<option value="{d}">{d:02d}</option>')
    day_html = '<select id="f-day" required>\n                ' + '\n                '.join(day_options) + '\n              </select>'

    # 2. Static options for f-year
    year_options = ['<option value="">YYYY</option>']
    for y in range(2026, 1939, -1):
        year_options.append(f'<option value="{y}">{y}</option>')
    year_html = '<select id="f-year" required>\n                ' + '\n                '.join(year_options) + '\n              </select>'

    # Replace f-day select
    day_regex = re.compile(r'<select id=["\']f-day["\'][^>]*>[\s\S]*?</select>')
    if not day_regex.search(content):
        print("ERROR: could not find f-day select")
        return
    content = day_regex.sub(day_html, content, count=1)

    # Replace f-year select
    year_regex = re.compile(r'<select id=["\']f-year["\'][^>]*>[\s\S]*?</select>')
    if not year_regex.search(content):
        print("ERROR: could not find f-year select")
        return
    content = year_regex.sub(year_html, content, count=1)

    # 3. Update calculateHeroProfile to call renderSaveProfileCard and syncCalculation
    old_reveal = """      // Reveal Results
      const resEl = document.getElementById('birth-results');
      resEl.style.display = 'block';
      resEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }"""

    new_reveal = """      // Reveal Results
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

    if old_reveal in content:
        content = content.replace(old_reveal, new_reveal, 1)
    else:
        print("WARNING: exact old_reveal not found, attempting regex replacement")
        content = re.sub(
            r"// Reveal Results[\s\S]*?resEl\.scrollIntoView\(\{\s*behavior:\s*['\"]smooth['\"],\s*block:\s*['\"]nearest['\"]\s*\}\);\s*\}",
            new_reveal,
            content,
            count=1
        )

    # 4. Update initClientComponents to add populateDateDropdownsFallback & auto-hydrate calculateHeroProfile
    old_init = """function initClientComponents() {
      initCharmAILauncher();
      initCookieConsent();

      // Ensure test mode token is set for workable testing
      try {
        if (!localStorage.getItem('nv_premium_token')) {
          localStorage.setItem('nv_premium_token', 'test_master_pass');
        }

        // Hydrate clientState and Hero form from localStorage if saved
        const raw = localStorage.getItem('nv_user_profile');
        if (raw) {
          const prof = JSON.parse(raw);
          Object.assign(clientState, prof);

          const fName = document.getElementById('f-name');
          const fDay = document.getElementById('f-day');
          const fMonth = document.getElementById('f-month');
          const fYear = document.getElementById('f-year');

          if (prof.name && fName && !fName.value) fName.value = prof.name;
          if (prof.day && fDay && !fDay.value) fDay.value = prof.day;
          if (prof.month && fMonth && !fMonth.value) fMonth.value = prof.month;
          if (prof.year && fYear && !fYear.value) fYear.value = prof.year;

          if (window.location.hash === '#charm-ai' && prof.driver) {
            seedCharmAiProfile();
          }
        }
      } catch (e) {
        console.warn('Profile hydration error:', e);
      }
    }"""

    new_init = """function populateDateDropdownsFallback() {
      const fDay = document.getElementById('f-day');
      if (fDay && fDay.options.length <= 1) {
        for (let d = 1; d <= 31; d++) {
          const opt = document.createElement('option');
          opt.value = String(d);
          opt.textContent = d < 10 ? '0' + d : String(d);
          fDay.appendChild(opt);
        }
      }
      const fYear = document.getElementById('f-year');
      if (fYear && fYear.options.length <= 1) {
        for (let y = 2026; y >= 1940; y--) {
          const opt = document.createElement('option');
          opt.value = String(y);
          opt.textContent = String(y);
          fYear.appendChild(opt);
        }
      }
    }

    function initClientComponents() {
      populateDateDropdownsFallback();
      initCharmAILauncher();
      initCookieConsent();

      // Ensure test mode token is set for workable testing
      try {
        if (!localStorage.getItem('nv_premium_token')) {
          localStorage.setItem('nv_premium_token', 'test_master_pass');
        }

        // Hydrate clientState and Hero form from localStorage if saved
        const raw = localStorage.getItem('nv_user_profile');
        if (raw) {
          const prof = JSON.parse(raw);
          Object.assign(clientState, prof);

          const fName = document.getElementById('f-name');
          const fDay = document.getElementById('f-day');
          const fMonth = document.getElementById('f-month');
          const fYear = document.getElementById('f-year');

          if (prof.name && fName && !fName.value) fName.value = prof.name;
          if (prof.day && fDay && !fDay.value) fDay.value = String(prof.day);
          if (prof.month && fMonth && !fMonth.value) fMonth.value = String(prof.month);
          if (prof.year && fYear && !fYear.value) fYear.value = String(prof.year);

          if (prof.driver && prof.conductor) {
            calculateHeroProfile();
          }

          if (window.location.hash === '#charm-ai' && prof.driver) {
            seedCharmAiProfile();
          }
        }
      } catch (e) {
        console.warn('Profile hydration error:', e);
      }
    }"""

    if old_init in content:
        content = content.replace(old_init, new_init, 1)
    else:
        print("WARNING: exact old_init not found, using regex")
        content = re.sub(
            r"function initClientComponents\(\)[\s\S]*?console\.warn\('Profile hydration error:', e\);\s*\}\s*\}",
            new_init,
            content,
            count=1
        )

    # 5. Add nv_profile_sync.js script tag before </body> if not present
    if '/static/js/nv_profile_sync.js' not in content:
        content = content.replace(
            '<script src="/static/js/nv_consent.js" defer></script>',
            '<script src="/static/js/nv_consent.js" defer></script>\n  <script src="/static/js/nv_profile_sync.js" defer></script>'
        )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: index.html updated successfully.")

if __name__ == '__main__':
    update_index_html()
