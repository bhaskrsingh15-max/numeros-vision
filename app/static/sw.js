// ============================================================
// NUMEROS VISION — SERVICE WORKER
// Single SW_VERSION used for headers, logs, and cache names
// ============================================================

const SW_VERSION = 'v6.3.0';
const CACHE_NAME = `numeros-static-${SW_VERSION}`;
const STATIC_CACHE = CACHE_NAME;

// Assets to cache individually on install (App Shell) - only public clean 200 URLs
const APP_SHELL = [
  '/',
  '/sample_roadmap/',
  '/reports_catalogue/',
  '/pricing/',
  '/about/',
  '/contact/',
  '/privacy/',
  '/terms/',
  '/refund-policy/',
  '/disclaimer/',
  '/accessibility/',
  '/methodology/',
  '/tools/life-path-calculator/',
  '/tools/lo-shu-grid/',
  '/tools/mobile-numerology/',
  '/tools/favourable-numbers/',
  '/tools/name-numerology/',
  '/tools/name-balancing/',
  '/tools/profession-calculator/',
  '/tools/property-numerology/',
  '/tools/vehicle-numerology/',
  '/tools/compatibility-calculator/',
  '/tools/blessing-years/',
  '/tools/baby-naming/',
  '/tools/business-alignment/',
  '/tools/logo-intelligence/',
  '/manifest.json',
  '/static/css/theme.css?v=5.4.0',
  '/static/css/roadmap_components.css?v=5.5.0',
  'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600;700&display=swap',
];

// Helper for fetch with real AbortController timeout
async function fetchWithTimeout(resource, options = {}, timeoutMs = 5000) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(resource, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  } catch (err) {
    clearTimeout(id);
    throw err;
  }
}

// ── INSTALL: Cache app shell individually so one failure does not empty shell
self.addEventListener('install', (event) => {
  console.log(`[SW ${SW_VERSION}] Installing Numeros Vision Service Worker`);
  event.waitUntil(
    caches.open(STATIC_CACHE).then(async (cache) => {
      await Promise.allSettled(
        APP_SHELL.map(async (url) => {
          try {
            const res = await fetch(url, { cache: 'no-cache' });
            if (res.ok) {
              await cache.put(url, res);
            }
          } catch (err) {
            console.warn(`[SW ${SW_VERSION}] Failed to cache ${url}:`, err);
          }
        })
      );
    }).then(() => self.skipWaiting())
  );
});

// ── ACTIVATE: Clean old caches on version bump
self.addEventListener('activate', (event) => {
  console.log(`[SW ${SW_VERSION}] Activating Numeros Vision Service Worker`);
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== STATIC_CACHE)
          .map(name => {
            console.log(`[SW ${SW_VERSION}] Deleting old cache:`, name);
            return caches.delete(name);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// ── MESSAGE LISTENER: Clear cache on logout or client request
self.addEventListener('message', (event) => {
  if (event.data && (event.data.action === 'CLEAR_CACHE' || event.data.action === 'LOGOUT')) {
    console.log(`[SW ${SW_VERSION}] Received ${event.data.action}: Purging all cached data`);
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(cacheNames.map(name => caches.delete(name)));
      }).then(() => {
        if (event.ports && event.ports[0]) {
          event.ports[0].postMessage({ success: true, version: SW_VERSION });
        }
      })
    );
  }
});

// ── FETCH: Routing strategy ───────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests and chrome-extension requests
  if (request.method !== 'GET') return;
  if (url.protocol === 'chrome-extension:') return;

  // 1. PRIVACY & DATA INTEGRITY GUARD: Strictly NEVER cache API calls, auth, orders, checkout, reports, or downloads (Network Only)
  if (
    url.pathname.startsWith('/api/') ||
    url.pathname.includes('/reports/download') ||
    url.pathname.includes('/checkout') ||
    url.pathname.endsWith('.pdf')
  ) {
    event.respondWith(fetch(request));
    return;
  }

  // 2. PRIVACY GUARD: Dashboard and user session pages are private; NEVER cache on shared devices
  if (
    url.pathname.startsWith('/dashboard') ||
    url.pathname.startsWith('/login') ||
    url.pathname.startsWith('/signup')
  ) {
    event.respondWith(fetch(request));
    return;
  }

  // 3. Public Static HTML Navigation: Network-First with AbortController timeout & offline fallback
  if (request.mode === 'navigate' || (request.headers.get('accept') && request.headers.get('accept').includes('text/html'))) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }

  // 4. External Fonts & CDNs: Cache First (rarely changes)
  if (
    url.hostname === 'fonts.googleapis.com' ||
    url.hostname === 'fonts.gstatic.com' ||
    url.hostname === 'unpkg.com' ||
    url.hostname === 'cdn.tailwindcss.com'
  ) {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
    return;
  }

  // 5. App static assets (CSS, JS, images): Stale-while-revalidate
  event.respondWith(staleWhileRevalidate(request));
});

// ── STRATEGIES ────────────────────────────────────────────────

async function networkFirstStrategy(request) {
  const cache = await caches.open(STATIC_CACHE);
  try {
    const networkResponse = await fetchWithTimeout(request.clone(), {}, 5000);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    return new Response(getOfflineFallbackHTML(), {
      status: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'X-Numeros-Offline': 'true',
        'X-SW-Version': SW_VERSION
      }
    });
  }
}

async function cacheFirstStrategy(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch {
    return new Response('Asset unavailable offline', { status: 503 });
  }
}

async function staleWhileRevalidate(request) {
  const url = new URL(request.url);
  const isStylesheet = url.pathname.endsWith('.css');
  const isScript = url.pathname.endsWith('.js');
  const isImage = url.pathname.endsWith('.png') || url.pathname.endsWith('.jpg') || url.pathname.endsWith('.svg') || url.pathname.endsWith('.ico');

  const cache = await caches.open(STATIC_CACHE);
  const cached = await cache.match(request);
  const fetchPromise = fetch(request).then((response) => {
    if (response.ok) cache.put(request, response.clone());
    return response;
  }).catch(() => null);

  if (cached) return cached;
  const netRes = await fetchPromise;
  if (netRes) return netRes;

  if (isStylesheet) {
    return new Response('', { status: 200, headers: { 'Content-Type': 'text/css' } });
  }
  if (isScript) {
    return new Response('', { status: 200, headers: { 'Content-Type': 'application/javascript' } });
  }
  if (isImage) {
    return new Response('', { status: 404 });
  }

  return new Response(
    getOfflineFallbackHTML(),
    { status: 200, headers: { 'Content-Type': 'text/html; charset=utf-8', 'X-SW-Version': SW_VERSION } }
  );
}

// ── PUSH NOTIFICATIONS ────────────────────────────────────────
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || '✦ NUMEROS VISION';
  const options = {
    body: data.body || 'Your daily celestial reading is ready.',
    icon: '/static/icons/icon-192.png',
    badge: '/static/icons/icon-72.png',
    vibrate: [200, 100, 200],
    data: { url: data.url || '/' },
    actions: [
      { action: 'read', title: 'Read Now' },
      { action: 'dismiss', title: 'Later' }
    ],
    tag: 'numeros-daily',
    requireInteraction: false
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  if (event.action === 'dismiss') return;
  const url = event.notification.data?.url || '/';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url === url && 'focus' in client) return client.focus();
      }
      if (clients.openWindow) return clients.openWindow(url);
    })
  );
});

// ── OFFLINE FALLBACK PAGE ─────────────────────────────────────
function getOfflineFallbackHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Offline · NUMEROS VISION</title>
  <style>
    :root {
      --bg-cream: #FFFDF7;
      --gold-dark: #8B6914;
      --gold-main: #C9A227;
      --ink: #523E28;
      --text-muted: #7A654D;
      --border-amber: rgba(201,162,39,0.3);
    }
    body {
      background: var(--bg-cream);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      text-align: center;
      padding: 24px;
      box-sizing: border-box;
    }
    .offline-card {
      background: #FFFFFF;
      border: 1px solid var(--border-amber);
      border-radius: 16px;
      padding: 40px 28px;
      max-width: 440px;
      box-shadow: 0 10px 30px rgba(82,62,40,0.06);
    }
    .icon {
      font-size: 2.8rem;
      color: var(--gold-main);
      margin-bottom: 16px;
      line-height: 1;
    }
    h1 {
      font-family: 'Cinzel', 'Cormorant Garamond', Georgia, serif;
      font-size: 1.45rem;
      color: var(--gold-dark);
      margin: 0 0 12px 0;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    p {
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.55;
      margin: 0 0 24px 0;
    }
    button {
      padding: 13px 30px;
      border-radius: 999px;
      background: linear-gradient(135deg, var(--gold-main), var(--gold-dark));
      border: none;
      color: #FFFFFF;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(201,162,39,0.25);
      transition: opacity 0.2s ease, transform 0.1s ease;
    }
    button:hover {
      opacity: 0.92;
      transform: translateY(-1px);
    }
  </style>
</head>
<body>
  <div class="offline-card">
    <div class="icon">✦</div>
    <h1>You are Currently Offline</h1>
    <p>You appear to have lost your internet connection. Saved readings will be accessible once connection is restored.</p>
    <button onclick="window.location.reload()">Retry Connection</button>
  </div>
</body>
</html>`;
}
