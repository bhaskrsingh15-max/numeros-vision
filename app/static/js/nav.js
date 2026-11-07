
// Ensure sticky bottom nav is never printed in any print dialog or PDF export
(function() {
  if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = '@media print { .nv-sticky-bottom-nav, nav.nv-sticky-bottom-nav, .nv-header, header, .nv-footer, footer:not(.page-footer), .no-print { display: none !important; visibility: hidden !important; } }';
    document.head.appendChild(style);
  }
})();

/**
 * Numeros Vision — Master Navigation & Table of Sections Controller
 * Brand: Anveil Every Charm
 */

function scrollTabs(delta) {
  const bar = document.getElementById('nav-tabs-bar');
  if (bar) {
    bar.scrollBy({ left: delta, behavior: 'smooth' });
    setTimeout(updateNavScrollButtons, 250);
  }
}

function updateNavScrollButtons() {
  const bar = document.getElementById('nav-tabs-bar');
  const leftBtn = document.querySelector('.nav-scroll-btn.left');
  const rightBtn = document.querySelector('.nav-scroll-btn.right');
  if (!bar) return;

  const hasOverflow = bar.scrollWidth > (bar.clientWidth + 4);
  if (hasOverflow) {
    bar.classList.add('has-overflow');
    if (leftBtn) {
      if (bar.scrollLeft > 8) {
        leftBtn.classList.add('visible');
      } else {
        leftBtn.classList.remove('visible');
      }
    }
    if (rightBtn) {
      if (bar.scrollLeft + bar.clientWidth < bar.scrollWidth - 8) {
        rightBtn.classList.add('visible');
      } else {
        rightBtn.classList.remove('visible');
      }
    }
  } else {
    bar.classList.remove('has-overflow');
    if (leftBtn) leftBtn.classList.remove('visible');
    if (rightBtn) rightBtn.classList.remove('visible');
  }
}

function toggleNavModal() {
  // Legacy stub - table of sections modal removed per requirements
  const modal = document.getElementById('all-tabs-modal');
  if (modal) modal.classList.toggle('active');
}

function openModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function toggleDrawer() {
  const d = document.getElementById('nav-drawer');
  const b = document.getElementById('hamburger-btn');
  if (d && b) {
    d.classList.toggle('open');
    b.classList.toggle('open');
  }
}

function closeDrawer() {
  const d = document.getElementById('nav-drawer');
  const b = document.getElementById('hamburger-btn');
  if (d) d.classList.remove('open');
  if (b) b.classList.remove('open');
}

function toggleNavDropdown(id, e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  const target = document.getElementById(id);
  const allGroups = document.querySelectorAll('.nav-dropdown-group, .nav-dropdown-wrapper');
  allGroups.forEach(g => {
    if (g !== target) g.classList.remove('open');
  });
  if (target) {
    target.classList.toggle('open');
  }
}

function toggleDrawerAccordion(id, e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  const group = document.getElementById(id);
  if (group) {
    group.classList.toggle('open');
  }
}

function toggleSectionsTableDropdown(e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
}

function closeAllDropdowns() {
  document.querySelectorAll('.nav-dropdown-group.open').forEach(g => g.classList.remove('open'));
  document.querySelectorAll('.nav-dropdown-wrapper.open').forEach(g => g.classList.remove('open'));
}

window.addEventListener('click', (e) => {
  if (!e.target.closest('.nav-dropdown-group') && !e.target.closest('.nav-dropdown-wrapper')) {
    closeAllDropdowns();
  }
});

function scrollToTop(e) {
  if (e && e.preventDefault) e.preventDefault();
  closeModal('all-tabs-modal');
  closeAllDropdowns();
  document.querySelectorAll('.nav-tab-link').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-tab-link[data-tab="home"]').forEach(t => t.classList.add('active'));
  document.querySelectorAll('.bottom-tab-item').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.bottom-tab-item[data-bottom-tab="home"]').forEach(t => t.classList.add('active'));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setTab(e, id) {
  if (e && e.preventDefault) e.preventDefault();
  closeModal('all-tabs-modal');
  closeAllDropdowns();
  const el = document.getElementById(id);
  if (el) {
    document.querySelectorAll('.nav-tab-link[data-tab]').forEach(t => t.classList.remove('active'));
    document.querySelectorAll(`.nav-tab-link[data-tab="${id}"]`).forEach(t => t.classList.add('active'));
    document.querySelectorAll('.bottom-tab-item[data-bottom-tab]').forEach(t => t.classList.remove('active'));
    document.querySelectorAll(`.bottom-tab-item[data-bottom-tab="${id}"]`).forEach(t => t.classList.add('active'));
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    // If on a sub-page, navigate back to home with anchor
    window.location.href = '/#' + id;
  }
}

// Scroll spy for smooth automatic tab highlighting across top & bottom bars
const _spySections = ['how-it-works', 'birth-profile', 'charm-ai', 'ai-oracle', 'plans', 'consultation'];
window.addEventListener('scroll', () => {
  let cur = 'home';
  if (window.scrollY < 200) {
    cur = 'home';
  } else {
    _spySections.forEach(id => {
      const el = document.getElementById(id);
      if (el && window.scrollY >= (el.offsetTop - 140)) cur = id;
    });
  }
  document.querySelectorAll('.nav-tab-link[data-tab]').forEach(t => t.classList.remove('active'));
  document.querySelectorAll(`.nav-tab-link[data-tab="${cur}"]`).forEach(t => t.classList.add('active'));
  document.querySelectorAll('.bottom-tab-item[data-bottom-tab]').forEach(t => t.classList.remove('active'));
  let bTab = cur;
  if (cur === 'how-it-works' || cur === 'birth-profile') bTab = 'home';
  if (cur === 'plans') bTab = 'consultation';
  document.querySelectorAll(`.bottom-tab-item[data-bottom-tab="${bTab}"]`).forEach(t => t.classList.add('active'));

  // Floating Back to Top visibility
  const topBtn = document.getElementById('back-to-top-btn');
  if (topBtn) {
    if (window.scrollY > 300) {
      topBtn.classList.add('visible');
    } else {
      topBtn.classList.remove('visible');
    }
  }
}, { passive: true });

// Close on overlay click & escape key + Nav Scroll initialization
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.modal-overlay').forEach(m => {
    m.addEventListener('click', e => { if (e.target === m) closeModal(m.id); });
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.active').forEach(m => closeModal(m.id));
      closeAllDropdowns();
    }
  });

  const tabsBar = document.getElementById('nav-tabs-bar');
  if (tabsBar) {
    tabsBar.scrollLeft = 0;
    tabsBar.addEventListener('scroll', updateNavScrollButtons, { passive: true });
    updateNavScrollButtons();
  }
  window.addEventListener('resize', updateNavScrollButtons, { passive: true });
});

// ── MASTER MOBILE & TABLET DRAWER NAVIGATION CONTROLLER ──
let _lastNavToggleTime = 0;

function syncHeaderHeight() {
  const header = document.querySelector('.nv-header');
  if (header) {
    const h = header.offsetHeight || 58;
    document.documentElement.style.setProperty('--nv-header-height', h + 'px');
  }
}

function ensureDrawerBackdrop() {
  let backdrop = document.getElementById('nv-drawer-backdrop');
  if (!backdrop) {
    backdrop = document.createElement('div');
    backdrop.id = 'nv-drawer-backdrop';
    backdrop.className = 'nv-drawer-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      closeMobileNav();
    });
    document.body.appendChild(backdrop);
  }
  return backdrop;
}

function closeMobileNav() {
  const menu = document.getElementById('nvNavMenu') || document.getElementById('nv-nav-menu') || document.querySelector('.nv-nav-menu');
  if (menu) {
    menu.classList.remove('active');
  }
  document.querySelectorAll('.nv-mobile-toggle').forEach(btn => {
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '☰';
  });
  const header = document.querySelector('.nv-header');
  if (header) {
    header.classList.remove('menu-open');
  }
  document.body.classList.remove('nv-nav-open');

  const backdrop = document.getElementById('nv-drawer-backdrop');
  if (backdrop) {
    backdrop.classList.remove('active');
  }

  // Restore active bottom tab indicator
  updateBottomNavActive();
}
window.closeMobileNav = closeMobileNav;

function toggleMobileNav(e) {
  const evt = e || window.event;
  if (evt) {
    if (evt.preventDefault) evt.preventDefault();
    if (evt.stopPropagation) evt.stopPropagation();
  }
  const now = Date.now();
  if (now - _lastNavToggleTime < 200) {
    return;
  }
  _lastNavToggleTime = now;

  const menu = document.getElementById('nvNavMenu') || document.getElementById('nv-nav-menu') || document.querySelector('.nv-nav-menu');
  if (!menu) return;

  syncHeaderHeight();
  const isOpen = menu.classList.toggle('active');

  document.querySelectorAll('.nv-mobile-toggle').forEach(btn => {
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    btn.innerHTML = isOpen ? '✕' : '☰';
  });

  const header = document.querySelector('.nv-header');
  if (header) {
    header.classList.toggle('menu-open', isOpen);
  }
  document.body.classList.toggle('nv-nav-open', isOpen);

  const backdrop = ensureDrawerBackdrop();
  if (backdrop) {
    backdrop.classList.toggle('active', isOpen);
  }

  // Synchronize bottom sticky navigation "Menu" tab
  document.querySelectorAll('.nv-bottom-nav-toggle').forEach(btn => {
    btn.classList.toggle('active', isOpen);
  });
  if (!isOpen) {
    updateBottomNavActive();
  }
}
window.toggleMobileNav = toggleMobileNav;
window.nvToggleMaster = toggleMobileNav;

function wireToggleButtons() {
  document.querySelectorAll('.nv-mobile-toggle').forEach(btn => {
    btn.onclick = toggleMobileNav;
  });
  document.querySelectorAll('.nv-bottom-nav-toggle').forEach(btn => {
    btn.onclick = toggleMobileNav;
  });
}

// Mobile and Tablet Accordion Submenu Controller
window.toggleNavAccordion = function(btn, e) {
  const evt = e || window.event;
  if (evt) {
    if (evt.preventDefault) evt.preventDefault();
    if (evt.stopPropagation) evt.stopPropagation();
  }
  const item = btn.closest('.nv-has-dropdown');
  if (!item) return;
  const isCurrentlyOpen = item.classList.contains('open');
  const parentMenu = item.closest('.nv-nav-menu');
  if (parentMenu) {
    parentMenu.querySelectorAll('.nv-has-dropdown.open').forEach(s => {
      if (s !== item) s.classList.remove('open');
    });
  }
  item.classList.toggle('open', !isCurrentlyOpen);
  btn.setAttribute('aria-expanded', !isCurrentlyOpen ? 'true' : 'false');
};

// Automatic Active Tab Highlighting on Sticky Bottom Nav
function updateBottomNavActive() {
  const path = window.location.pathname.toLowerCase();
  const hash = window.location.hash;
  const items = document.querySelectorAll('.nv-bottom-nav-item[data-nav], .nv-bottom-item[data-nav]');
  items.forEach(item => {
    const nav = item.getAttribute('data-nav');
    let isActive = false;
    if (nav === 'home' && (path === '/' || path === '/index.html' || path === '') && !hash) {
      isActive = true;
    } else if ((nav === 'calculate' || nav === 'tools' || nav === 'calculators') && (path.includes('calculator') || path.includes('/tools/')) && !path.includes('catalogue')) {
      isActive = true;
    } else if (nav === 'charm' && (path.includes('charm') || hash === '#charm-ai')) {
      isActive = true;
    } else if (nav === 'reports' && (path.includes('reports') || path.includes('catalogue'))) {
      isActive = true;
    } else if (nav === 'account' && (path.includes('dashboard') || path.includes('account') || path.includes('login') || path.includes('signup'))) {
      isActive = true;
    } else if (nav === 'home' && (hash === '#birth-profile' || hash === '#calculator-card')) {
      isActive = true;
    }
    item.classList.toggle('active', isActive);
  });
}
window.updateBottomNavActive = updateBottomNavActive;

// Mobile & Tablet Sticky Bottom Navigation Bar Auto-Injector
function initStickyBottomNav() {
  ensureDrawerBackdrop();
  if (document.querySelector('.nv-sticky-bottom-nav')) {
    updateBottomNavActive();
    return;
  }
  const nav = document.createElement('nav');
  nav.className = 'nv-sticky-bottom-nav';
  nav.setAttribute('aria-label', 'Mobile and Tablet Navigation');
  nav.innerHTML = `
    <a href="/" class="nv-bottom-nav-item" data-nav="home" title="Home">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>
    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="calculate" title="Calculate">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Calculate</span>
    </a>
    <a href="/charm_ai.html" class="nv-bottom-nav-item nv-bottom-nav-center" data-nav="charm" title="Charm AI">
      <div class="nv-bottom-center-btn">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#FFFFFF" stroke-width="2.2" style="display:block; stroke:#FFFFFF !important; transform:none !important;"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z" stroke="#FFFFFF"/></svg>
      </div>
      <span>Charm AI</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Reports">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      <span>Reports</span>
    </a>
    <a href="/dashboard/" class="nv-bottom-nav-item" data-nav="account" title="Account">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Account</span>
    </a>
  `;
  document.body.appendChild(nav);
  updateBottomNavActive();
}
window.initStickyBottomNav = initStickyBottomNav;

// Auto-wire event listeners
document.addEventListener('DOMContentLoaded', () => {
  syncHeaderHeight();
  ensureDrawerBackdrop();
  window.addEventListener('resize', syncHeaderHeight, { passive: true });

  // Close mobile menu when tapping anywhere outside (fallback for clicks outside backdrop)
  document.addEventListener('click', (e) => {
    const menu = document.getElementById('nvNavMenu') || document.getElementById('nv-nav-menu') || document.querySelector('.nv-nav-menu');
    if (menu && menu.classList.contains('active')) {
      const isInsideMenu = menu.contains(e.target);
      const isToggle = e.target.closest('.nv-mobile-toggle') || e.target.closest('.nv-bottom-nav-toggle');
      if (!isInsideMenu && !isToggle) {
        closeMobileNav();
      }
    }
  });

  // Automatically close mobile menu when clicking a destination link
  document.addEventListener('click', (e) => {
    const link = e.target.closest('.nv-nav-menu a');
    if (link && !link.classList.contains('nv-dropdown-toggle')) {
      closeMobileNav();
    }
  });

  // Initialize Sticky Bottom Nav & Wire Buttons
  initStickyBottomNav();
  wireToggleButtons();
});

// Run immediately if DOM is already parsed
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  syncHeaderHeight();
  ensureDrawerBackdrop();
  initStickyBottomNav();
  wireToggleButtons();
}

// Auto-load unified consent manager if not already present
(function () {
  if (!window.nvConsent && !document.querySelector('script[src*="nv_consent.js"]')) {
    const s = document.createElement('script');
    s.src = '/static/js/nv_consent.js';
    s.defer = true;
    document.head.appendChild(s);
  }
})();

// Auto-load PWA install controller if not already present
(function () {
  if (!document.querySelector('script[src*="pwa_install.js"]')) {
    const s = document.createElement('script');
    s.src = '/static/js/pwa_install.js?v=4.7.3';
    s.defer = true;
    document.head.appendChild(s);
  }
})();

