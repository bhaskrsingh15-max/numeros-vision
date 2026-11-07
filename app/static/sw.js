// ============================================================
// NUMEROS VISION — SERVICE WORKER v5.2.0-brand-uniform
// Handles: Offline caching, push notifications, background sync
// ============================================================

const CACHE_NAME = 'numeros-static-v5.5.0-charm-logo-canonical';
const STATIC_CACHE = 'numeros-static-v5.5.0-charm-logo-canonical';
const API_CACHE = 'numeros-api-v5.5.0-charm-logo-canonical';

// Assets to cache immediately on install (App Shell)
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
  '/practitioner/',
  '/tools/life-path-calculator/',
  '/tools/lo-shu-grid/',
  '/tools/mobile-numerology/',
  '/tools/lucky-number/',
  '/tools/name-numerology/',
  '/tools/name-balancing/',
  '/tools/profession-calculator/',
  '/tools/property-numerology/',
  '/tools/vehicle-numerology/',
  '/tools/compatibility-calculator/',
  '/tools/blessing-years/',
  '/tools/baby-naming/',
  '/tools/business-alignment/',
  '/tools/logo-studio/',
  '/manifest.json',
  '/manifest.webmanifest',
  '/static/css/theme.css?v=4.8.0',
  '/static/css/roadmap_components.css?v=4.8.0',
  'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600;700&display=swap',
];



// ── INSTALL: Cache app shell ──────────────────────────────────
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Numeros Vision Service Worker v5.2.0-brand-uniform');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(APP_SHELL).catch((err) => {
        console.warn('[SW] Failed to cache some shell assets:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// ── ACTIVATE: Clean old caches ────────────────────────────────
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Numeros Vision Service Worker v5.0.0-clean');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== STATIC_CACHE)
          .map(name => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// ── FETCH: Routing strategy ───────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests and chrome-extension requests
  if (request.method !== 'GET') return;
  if (url.protocol === 'chrome-extension:') return;

  // 1. PRIVACY GUARD: Strictly NEVER cache API calls, report downloads, or PDFs
  if (url.pathname.startsWith('/api/') || url.pathname.includes('/reports/download') || url.pathname.endsWith('.pdf')) {
    event.respondWith(fetch(request));
    return;
  }

  // 2. PRIVACY GUARD: Dashboard navigation is private to the session; NEVER cache on shared devices
  if (url.pathname.startsWith('/dashboard')) {
    event.respondWith(fetch(request));
    return;
  }

  // 3. Public Static HTML Navigation: Network-First
  if (request.mode === 'navigate' || (request.headers.get('accept') && request.headers.get('accept').includes('text/html'))) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }

  // Google Fonts: Cache First (rarely changes)
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
    return;
  }

  // External CDN (Lucide icons, etc.): Cache First
  if (url.hostname === 'unpkg.com' || url.hostname === 'cdn.tailwindcss.com') {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
    return;
  }

  // App pages & assets: Stale-while-revalidate
  event.respondWith(staleWhileRevalidate(request));
});

// ── STRATEGIES ────────────────────────────────────────────────

async function networkFirstStrategy(request) {
  const cache = await caches.open(STATIC_CACHE);
  try {
    const networkResponse = await fetch(request.clone(), { timeout: 5000 });
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    const cached = await cache.match(request);
    if (cached) return cached;
    return new Response(
      JSON.stringify({ error: 'offline', message: 'You are offline. Please check your connection.' }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    );
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
    { headers: { 'Content-Type': 'text/html' } }
  );
}

// ── PUSH NOTIFICATIONS ────────────────────────────────────────
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  const title = data.title || '✦ Numeros Vision';
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

// ── BACKGROUND SYNC ───────────────────────────────────────────
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-booking') {
    event.waitUntil(syncPendingBookings());
  }
  if (event.tag === 'sync-question') {
    event.waitUntil(syncPendingQuestions());
  }
});

async function syncPendingBookings() {
  // Sync any bookings saved to IndexedDB while offline
  console.log('[SW] Syncing pending bookings...');
}

async function syncPendingQuestions() {
  console.log('[SW] Syncing pending Charm AI questions...');
}

// ── OFFLINE FALLBACK ──────────────────────────────────────────
function getOfflineFallbackHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Numeros Vision — Offline</title>
  <style>
    body { background: #06030f; color: #f0eaff; font-family: 'Inter', sans-serif;
           display: flex; align-items: center; justify-content: center;
           min-height: 100vh; margin: 0; text-align: center; padding: 24px; }
    .icon { font-size: 4rem; margin-bottom: 20px; }
    h1 { font-size: 1.5rem; margin-bottom: 12px; }
    p { color: rgba(240,234,255,0.5); font-size: 0.9rem; line-height: 1.6; max-width: 340px; }
    button { margin-top: 24px; padding: 14px 28px; border-radius: 14px;
             background: linear-gradient(135deg,#d4a843,#c9973a); border: none;
             color: #06030f; font-weight: 700; cursor: pointer; font-size: 0.85rem; }
  </style>
</head>
<body>
  <div>
    <div class="icon">✦</div>
    <h1>You're Offline</h1>
    <p>The stars are still aligned for you. Please check your internet connection and try again.</p>
    <button onclick="location.reload()">Try Again</button>
  </div>
</body>
</html>`;
}
