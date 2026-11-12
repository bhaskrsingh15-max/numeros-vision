/* Numeros Vision · Anveil module · v1
   Vanilla JS, no dependencies. Load after nv-anveil.css.
   Public API: NVAnveil.configure(), mountOrbit(), mountReport().
   Prices shown here are display only: your server must look up the real
   amount from its own table when it creates the payment order. */
(function (global) {
  'use strict';

  // ---------- 1. Configuration (edit this block) ----------
  const CONFIG = {
    logo: '/assets/brand/nv-logo-watermark.svg', // full circle logo, watermark in the orbit centre
    checkoutUrl: '/checkout/',              // receives ?tier=&svc= only; the birth date travels in sessionStorage / POST body, never in the URL
    packageUrl: '/package/',                // "What's included" page, same params
    includeCoreInGrid: false, // Approved single rule: 8 raw non-zero DDMMYYYY digits only                // your method: plot Mulank + Bhagyank too
    tiers: {
      e: { sku: 'report_premium', label: 'Anveil every charm', descriptor: 'Complete Numerology Report, 32 pages', price: 'Coming soon, notify me', mrp: '', pages: 'Complete Numerology Report, 32 pages', per: '', waitlistOnly: true },
      g: { sku: 'report_advanced', label: 'Anveil my glowing charms', descriptor: 'Advanced Numerology Report, 12 pages', price: 'Coming soon, notify me', mrp: '', pages: 'Advanced Numerology Report, 12 pages', per: '', waitlistOnly: true },
      a: { sku: 'report_basic', label: 'Anveil my alignments', descriptor: 'Basic Numerology Report, 3 pages', price: '₹399', mrp: '', pages: 'Basic Numerology Report, 3 pages', per: '', waitlistOnly: false }
    },
    // One row per calculator. Fill name, price, pages and key numbers.
    services: {}
  };

  // ---------- 2. Numerology data ----------
  const ORDER = [4, 9, 2, 3, 5, 7, 8, 1, 6];
  const CHARM = { 1: 'Expression', 2: 'Harmony', 3: 'Wisdom', 4: 'Abundance', 5: 'Balance', 6: 'Grace', 7: 'Mystic', 8: 'Legacy', 9: 'Courage' };
  const PLANET = { 1: ['Sun', 'Surya'], 2: ['Moon', 'Chandra'], 3: ['Jupiter', 'Guru'], 4: ['Rahu', 'North Node'], 5: ['Mercury', 'Budh'], 6: ['Venus', 'Shukra'], 7: ['Ketu', 'South Node'], 8: ['Saturn', 'Shani'], 9: ['Mars', 'Mangal'] };
  // Soft palette for the 3D animation only: highlight, base, edge, text on sphere
  const SOFT = {
    1: ['#FFE9C7', '#F2B66D', '#C98A3E', '#3B2F1A'], 2: ['#FFFFFF', '#E9EDF1', '#B5BEC7', '#3B3F46'],
    3: ['#FFF6CF', '#F1D77A', '#C7A842', '#3B2F1A'], 4: ['#F1F0EE', '#B9B6B1', '#8C8984', '#2F2C28'],
    5: ['#E3F4E6', '#93CBA0', '#5E9C6E', '#1F3A27'], 6: ['#FFFFFF', '#F6F0E8', '#D3C4B0', '#3B2F1A'],
    7: ['#E5ECF8', '#9DB3D9', '#6A82AE', '#1E2B44'], 8: ['#9A9792', '#6B6864', '#4A4743', '#FFFFFF'],
    9: ['#FBE0DA', '#E39A8E', '#B9675B', '#3B1F1A']
  };
  const C = (x, y, r) => `M${x - r} ${y}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0`;
  const GLYPH = {
    1: C(12, 12, 8) + C(12, 12, 1.2), 2: 'M15 4a8 8 0 1 0 0 16a6.5 6.5 0 0 1 0-16z', 3: 'M6 8c1-4 7-4 6 1l-6 7h12M15 4v17',
    4: 'M8 17a5 5 0 1 1 8 0' + C(7, 18.5, 1.8) + C(17, 18.5, 1.8), 5: C(12, 11, 4) + 'M12 15v6M9 18h6M8 3a4 4 0 0 0 8 0',
    6: C(12, 9, 5) + 'M12 14v7M9 18h6', 7: 'M8 7a5 5 0 1 0 8 0' + C(7, 5.5, 1.8) + C(17, 5.5, 1.8),
    8: 'M7 5h7M10 2v13M10 11c1-3 6-3 6 1c0 3-3 4-2 8', 9: C(10, 14, 5) + 'M13.5 10.5L20 4M15 4h5v5'
  };
  const sphere = n => `radial-gradient(circle at 34% 28%, ${SOFT[n][0]} 0%, ${SOFT[n][1]} 52%, ${SOFT[n][2]} 100%)`;
  const isDob = v => /^\d{4}-\d{2}-\d{2}$/.test(v || '');
  const reduce = x => { while (x > 9) x = String(x).split('').reduce((a, d) => a + Number(d), 0); return x; };

  // Counts each digit 1-9 in the grid. With includeCoreInGrid, Mulank and Bhagyank are added (your method).
  function computeGrid(dob) {
    const [y, m, d] = dob.split('-');
    const digits = (d + m + y).split('').filter(x => x !== '0').map(Number);
    if (CONFIG.includeCoreInGrid) {
      digits.push(reduce(Number(d)));
      digits.push(reduce(digits.slice(0, -1).reduce((a, b) => a + b, 0)));
    }
    const counts = {}; digits.forEach(x => { counts[x] = (counts[x] || 0) + 1; });
    return counts;
  }
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const randomDob = () => { const y = 1965 + Math.floor(Math.random() * 41), m = 1 + Math.floor(Math.random() * 12), d = 1 + Math.floor(Math.random() * 28); return `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`; };
  const fmt = dob => { const [y, m, d] = dob.split('-'); return `${d}-${m}-${y}`; };
  const lowPower = () => (navigator.deviceMemory && navigator.deviceMemory <= 2) || (navigator.connection && navigator.connection.saveData);

  // ---------- 3. Living orbit ----------
  // mountOrbit(container, { scale, mode: 'sample' | 'personal', dob, onlyPresent })
  function mountOrbit(container, opts) {
    const o = Object.assign({ scale: 1, mode: 'sample', dob: null, onlyPresent: false, caption: true }, opts || {});
    const box = el('div', 'nv-orbit-box');
    box.style.width = 680 * o.scale + 'px'; box.style.height = 700 * o.scale + 'px';
    const root = el('div', 'nv-orbit'); root.style.transform = `scale(${o.scale})`;
    root.innerHTML =
      `<svg class="nv-seal" viewBox="0 0 680 680" aria-hidden="true"><defs><path id="nv-seal-path" d="M340,340 m-322,0 a322,322 0 1,1 644,0 a322,322 0 1,1 -644,0"/></defs>` +
      `<circle cx="340" cy="340" r="336" fill="none" stroke="#D9C48A"/><circle cx="340" cy="340" r="306" fill="none" stroke="#E8DCB8"/>` +
      `<text font-family="Cinzel, serif" font-size="13" letter-spacing="4" fill="#9C7A22" opacity=".6"><textPath href="#nv-seal-path" textLength="2010" lengthAdjust="spacing">NUMEROS VISION ✦ ANVEIL EVERY CHARM ✦ NUMEROS VISION ✦ ANVEIL EVERY CHARM ✦ NUMEROS VISION ✦ ANVEIL EVERY CHARM ✦</textPath></text></svg>` +
      `<img class="nv-logo" src="${CONFIG.logo}" alt="" aria-hidden="true">`;
    const ring = el('div', 'nv-ring'); const plane = el('div', 'nv-plane');
    root.append(ring, plane); box.append(root); container.append(box);
    const cap = o.caption ? el('p', 'nv-orbit-caption') : null; if (cap) container.append(cap);

    const chips = {}, tiles = {};
    for (let n = 1; n <= 9; n++) {
      const dot = el('div', 'nv-dot');
      const b = el('button', 'nv-chip', `<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${GLYPH[n]}"/></svg><span>${n}</span>`);
      b.type = 'button'; b.style.background = sphere(n); b.style.border = `1px solid ${SOFT[n][2]}`; b.style.color = SOFT[n][3];
      b.addEventListener('mouseenter', () => say(n)); b.addEventListener('click', () => say(n));
      dot.append(b); ring.append(dot); chips[n] = { dot, b };
    }
    ORDER.forEach(n => { const t = el('div', 'nv-ptile'); plane.append(t); tiles[n] = t; });

    let counts = {}, personal = false;
    function say(n) {
      if (!cap) return;
      const k = counts[n];
      cap.textContent = `${personal ? 'Your ' : ''}${n} · ${PLANET[n][0]} (${PLANET[n][1]}) · ${CHARM[n]} Charm · ${k ? 'glowing' : 'veiled'}`;
    }
    function render(dob, isPersonal) {
      counts = computeGrid(dob); personal = isPersonal;
      let lit = 0;
      for (let n = 1; n <= 9; n++) {
        const k = counts[n] || 0, a = (n - 1) * 40 * Math.PI / 180, r = k ? 232 : 262;
        const c = chips[n];
        c.dot.style.left = Math.round(280 + r * Math.sin(a) - 26) + 'px';
        c.dot.style.top = Math.round(280 - r * Math.cos(a) - 26) + 'px';
        c.dot.style.transitionDelay = k ? (0.25 * lit++) + 's' : '0s';
        c.b.className = 'nv-chip ' + (k ? 'is-lit' : (o.onlyPresent ? 'is-dim is-ghost' : 'is-dim'));
        c.b.style.boxShadow = k ? `0 0 0 3px #FBF8EF, 0 0 16px ${SOFT[n][2]}99` : 'none';
        c.b.setAttribute('aria-label', `${n}, ${PLANET[n][0]}, ${CHARM[n]} Charm, ${k ? 'glowing' : 'veiled'}`);
        c.b.querySelector('span').textContent = (o.onlyPresent && !k) ? '' : n;
        if (o.onlyPresent && !k) c.b.querySelector('svg').style.visibility = 'hidden';
      }
      ORDER.forEach(n => {
        const k = counts[n] || 0, t = tiles[n];
        if (!k) { t.className = 'nv-ptile is-veiled nv-sheen'; t.style.cssText = ''; t.innerHTML = `<span>${n}</span><small>Veiled</small>`; return; }
        t.className = 'nv-ptile';
        t.style.background = '#fff'; t.style.border = `2px solid ${SOFT[n][2]}`; t.style.color = '#3B2F1A';
        t.style.boxShadow = '0 10px 24px rgba(122,92,18,.15)';
        t.innerHTML = `<i class="nv-core" style="background:${sphere(n)};box-shadow:0 0 10px ${SOFT[n][2]}aa"></i><span>${String(n).repeat(Math.min(k, 4))}</span><small>${CHARM[n]}${k > 1 ? ' ×' + k : ''}</small>`;
      });
      if (cap) cap.textContent = isPersonal ? 'Your glowing energies move inward to your grid' : 'Tap any planet to see its charm';
    }
    function setActive(n) {
      for (let i = 1; i <= 9; i++) chips[i].b.classList.toggle('is-active', i === n);
      ORDER.forEach(i => { const k = counts[i]; if (k) tiles[i].style.border = `${i === n ? 4 : 2}px solid ${i === n ? SOFT[i][1] : SOFT[i][2]}`; });
      if (cap && n) cap.textContent = `Your ${PLANET[n][0]} (${PLANET[n][1]}) lights your ${n} · ${CHARM[n]} Charm`;
    }

    // Sample mode rotates random charts until a personal date arrives
    let sampleTimer = null;
    if (o.mode === 'sample' && !isDob(o.dob)) {
      render(randomDob(), false);
      sampleTimer = setInterval(() => render(randomDob(), false), 7000);
    } else render(o.dob, true);

    // Pause off-screen and on low-power devices
    if (lowPower()) root.classList.add('nv-paused');
    if ('IntersectionObserver' in global) new IntersectionObserver(es => es.forEach(e => root.classList.toggle('nv-paused', !e.isIntersecting || lowPower()))).observe(box);

    return {
      setPersonal(dob) {                       // call when the visitor enters a valid date
        if (!isDob(dob)) return;
        clearInterval(sampleTimer); sampleTimer = null;
        ORDER.forEach(n => { tiles[n].className = 'nv-ptile is-veiled nv-sheen'; tiles[n].innerHTML = `<span>${n}</span>`; });
        if (cap) cap.textContent = 'Reading your birth date…';
        setTimeout(() => render(dob, true), 800);
      },
      setActive, counts: () => counts,
      destroy() { clearInterval(sampleTimer); container.innerHTML = ''; }
    };
  }

  // ---------- 4. Free report: tap-to-Anveil grid + price cards ----------
  // mountReport({ grid, prices, teaser, orbit, dob, svc })
  function mountReport(p) {
    const svc = CONFIG.services[p.svc] ? p.svc : 'general';
    const S = CONFIG.services[svc] || null;
    const counts = computeGrid(p.dob);
    let sel = null, view = 'charms', engaged = false, timers = [];
    const go = (url, tier) => { saveDob(p.dob); location.href = `${url}?tier=${encodeURIComponent(tier)}&svc=${encodeURIComponent(svc)}`; };
    const tierFor = n => view === 'align' ? 'a' : (S ? svc : (counts[n] ? 'g' : 'e'));
    const resolveTierDisplay = t => {
      if (S && t === svc) return { label: S.label || S.name, price: S.price, mrp: S.mrp || '', pages: S.pages || '', per: '', launchCopy: '', waitlistOnly: false };
      const base = CONFIG.tiers[t];
      if (global.NV_PRICING && base && base.sku) {
        const waitlistOnly = typeof global.NV_PRICING.isNotifyMeTier === 'function' && global.NV_PRICING.isNotifyMeTier(base.sku);
        if (waitlistOnly) {
          const wlLabel = typeof global.NV_PRICING.getWaitlistLabel === 'function' ? global.NV_PRICING.getWaitlistLabel() : 'Coming soon, notify me';
          return {
            label: base.label,
            price: wlLabel,
            mrp: '',
            pages: base.descriptor || base.pages,
            per: '',
            launchCopy: '',
            waitlistOnly: true
          };
        }
        const activePrice = global.NV_PRICING.formatPrice(base.sku);
        const struck = global.NV_PRICING.getStruckMrp(base.sku);
        const launchCopy = typeof global.NV_PRICING.formatLaunchOfferCopy === 'function'
          ? global.NV_PRICING.formatLaunchOfferCopy(base.sku)
          : '';
        return {
          label: base.label,
          price: activePrice,
          mrp: struck ? ('₹' + Number(struck).toLocaleString('en-IN')) : '',
          pages: base.descriptor || base.pages,
          per: '',
          launchCopy,
          waitlistOnly: false
        };
      }
      return Object.assign({ launchCopy: '', waitlistOnly: Boolean(base && base.waitlistOnly) }, base);
    };
    const priceOf = t => resolveTierDisplay(t).price;

    // Grid
    const grid = el('div', 'nv-grid'); p.grid.append(grid);
    const cells = {};
    ORDER.forEach(n => {
      const b = el('button', 'nv-cell'); b.type = 'button'; cells[n] = b; grid.append(b);
      b.addEventListener('click', () => tap(n));
    });
    function drawCells() {
      ORDER.forEach(n => {
        const k = counts[n] || 0, b = cells[n], open = sel === n;
        const focus = S && S.focus.indexOf(n) >= 0;
        const tDisp = resolveTierDisplay(tierFor(n));
        if (k) {
          b.className = 'nv-cell ' + (k > 1 ? 'is-radiant' : 'is-glow');
          b.innerHTML = `<span class="nv-num">${String(n).repeat(Math.min(k, 4))}</span><span class="nv-name">${CHARM[n]}</span>` +
            (open && view !== 'align' ? `<span class="nv-strip">${tDisp.waitlistOnly ? tDisp.price : ('Go deeper · ' + tDisp.price)} →</span>` : '');
          b.setAttribute('aria-label', `${CHARM[n]} Charm ${n}, glowing`);
        } else {
          b.className = 'nv-cell is-veiled' + (open ? ' is-open' : '');
          b.innerHTML = `<span class="nv-under"><span>${view === 'align' ? 'Your alignment' : (S ? S.name.split(' ')[0] + ' reading' : 'Every charm')}</span><b>${tDisp.price}</b><span>${tDisp.waitlistOnly ? 'Join waitlist →' : 'Anveil now →'}</span></span>` +
            `<span class="nv-shutter"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>Tap to Anveil${focus ? `<span class="nv-tag">Key for ${S.name.split(' ')[0].toLowerCase()}</span>` : ''}</span>`;
          b.setAttribute('aria-label', open ? `${tDisp.price}` : 'Veiled charm, locked, tap to Anveil');
        }
      });
    }
    function tap(n) {
      clearHints();
      if (sel === n) { go(CONFIG.checkoutUrl, tierFor(n)); return; }   // second tap = buy
      sel = n; engaged = true; drawCells(); drawPrices(); drawTeaser();
      track('nv_charm_tap', { n, veiled: !counts[n], svc });
    }

    // Hint ladder: shimmer 1.5s, breathing 3s, spotlight + tooltip 5s, finger 8s
    function clearHints() { timers.forEach(clearTimeout); timers = []; grid.classList.remove('is-shimmer', 'is-breathing'); grid.querySelectorAll('.nv-tip,.nv-finger').forEach(x => x.remove()); Object.values(cells).forEach(c => c.classList.remove('is-spot')); }
    function startHints() {
      const veiled = ORDER.filter(n => !counts[n]);
      const spot = [4, 5].find(n => !counts[n]) || veiled[0]; if (!spot) return;
      const i = ORDER.indexOf(spot), x = (i % 3) * 110, y = Math.floor(i / 3) * 110;
      timers.push(setTimeout(() => !engaged && grid.classList.add('is-shimmer'), 1500));
      timers.push(setTimeout(() => { if (!engaged) { grid.classList.remove('is-shimmer'); grid.classList.add('is-breathing'); } }, 3200));
      timers.push(setTimeout(() => { if (engaged) return; cells[spot].classList.add('is-spot'); const t = el('div', 'nv-tip', 'A charm is veiled here. Tap to Anveil'); t.style.left = Math.max(-40, x - 40) + 'px'; t.style.top = (y - 42) + 'px'; grid.append(t); }, 5200));
      timers.push(setTimeout(() => { if (engaged) return; const f = el('div', 'nv-finger', '<svg width="34" height="34" viewBox="0 0 24 24" fill="#FBF8EF" stroke="#3B2F1A" stroke-width="1.5" aria-hidden="true"><path d="M9 11V5a1.5 1.5 0 013 0v6m0-1a1.5 1.5 0 013 0v1m0 0a1.5 1.5 0 013 0v4c0 3-2 6-5 6h-1c-2 0-3-1-4-2l-3-4a1.5 1.5 0 012-2l2 2V11"/></svg>'); f.style.left = (x + 46) + 'px'; f.style.top = (y + 46) + 'px'; grid.append(f); }, 8000));
    }

    // Price cards
    function drawPrices() {
      if (!p.prices) return;
      const keys = S ? [svc, 'e', 'a'] : ['e', 'g', 'a'];
      const matchT = sel || view === 'align' ? tierFor(sel) : (S ? svc : null);
      const selVeiled = sel && !counts[sel] && view !== 'align';
      p.prices.innerHTML = '';
      keys.forEach(t => {
        const T = resolveTierDisplay(t);
        const featured = S ? t === svc : t === 'e', match = t === matchT, notFor = selVeiled && t === 'g';
        const tag = (S && t === svc) ? `For your ${S.name.split(' ')[0].toLowerCase()} question` : (match ? 'Matches the charm you tapped' : (t === 'e' ? 'Best value' : ''));
        const cover = notFor ? 'Covers your glowing charms only, not this veiled one'
          : (selVeiled && t === 'e') ? 'Unlocks this veiled charm: its number, gifts and remedies, plus all 9 charms'
          : (S && t === svc) ? `Focused on ${S.name.toLowerCase()}` : '';
        const card = el('div', 'nv-price' + (featured ? ' is-featured' : '') + (match ? ' is-match' : '') + (notFor ? ' is-notfor' : ''));
        card.innerHTML =
          `<div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap"><strong style="font-weight:500">${T.label}</strong>${tag ? `<span class="nv-pill${match ? ' is-match' : ''}">${tag}</span>` : ''}</div>` +
          `<div style="font-size:12px;color:#7A654D;margin-top:2px">${T.pages}</div>` +
          `<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap"><span class="nv-amt">${T.price}</span>${T.mrp ? `<s>${T.mrp}</s>` : ''}</div>` +
          (T.launchCopy ? `<div style="font-size:11.5px;color:#7A654D">${T.launchCopy}</div>` : '') +
          (cover ? `<p style="margin:0;font-size:13px">${cover}</p>` : '');
        const buyLabel = T.waitlistOnly ? T.price : `Anveil now · ${T.price}`;
        const buy = el('button', 'nv-btn', buyLabel); buy.type = 'button';
        buy.addEventListener('click', () => { track('select_package', { tier: t, svc, value: T.price }); go(CONFIG.checkoutUrl, t); });
        const info = el('a', '', "What's included"); info.href = `${CONFIG.packageUrl}?tier=${t}&svc=${svc}`; info.addEventListener('click', () => saveDob(p.dob)); info.style.cssText = 'text-align:center;font-size:13px';
        card.append(buy, info); p.prices.append(card);
      });
    }

    // Teaser panel (optional element)
    function drawTeaser() {
      if (!p.teaser) return;
      const glow = ORDER.filter(n => counts[n]);
      if (!sel) { p.teaser.innerHTML = `<h3>${glow.length} charms glow in your grid</h3><p>And ${9 - glow.length} are veiled, each holding a gift waiting for you. Tap any charm to begin.</p>`; return; }
      const k = counts[sel];
      p.teaser.innerHTML = k
        ? `<h3>Your ${CHARM[sel]} Charm ${k > 1 ? 'shines ×' + k : 'glows'}</h3><p>Planet: ${PLANET[sel][0]} (${PLANET[sel][1]}). Your free reading continues below; the paid reading goes deeper.</p>`
        : `<h3>A charm is veiled here</h3><p>Its number, its meaning for you and how to Anveil it are in your reading. Tap the charm again to Anveil it now, or choose below.</p>`;
    }

    // Sync orbit highlight with grid numbers
    let pulse = 0, syncTimer = null;
    if (p.orbit) {
      const present = Object.keys(counts).map(Number).sort((a, b) => a - b);
      syncTimer = setInterval(() => {
        const n = present[pulse++ % present.length]; p.orbit.setActive(n);
        ORDER.forEach(i => { cells[i].style.boxShadow = i === n ? `0 0 0 3px #fff, 0 0 0 6px ${SOFT[i][2]}cc, 0 0 16px ${SOFT[i][2]}88` : ''; });
      }, 1900);
    }

    drawCells(); drawPrices(); drawTeaser(); startHints();
    return {
      setView(v) { view = v === 'align' ? 'align' : 'charms'; sel = null; drawCells(); drawPrices(); },
      destroy() { clearHints(); clearInterval(syncTimer); }
    };
  }

  // Analytics hook: replace with your GA4 / CDP call
  // Birth date is personal data: keep it out of URLs (SEO + privacy). It stays in this browser tab and is POSTed to the server at checkout.
  function saveDob(d) { try { sessionStorage.setItem('nv_dob', d); } catch (e) {} }
  function loadDob() { try { return sessionStorage.getItem('nv_dob'); } catch (e) { return null; } }
  function track(name, data) { if (typeof global.nvTrack === 'function') { global.nvTrack(name, data || {}); } }

  global.NVAnveil = {
    configure: o => Object.assign(CONFIG, o || {}),
    mountOrbit, mountReport, computeGrid, saveDob, loadDob, randomDob, fmt, isDob, CHARM, PLANET, SOFT
  };
})(window);
