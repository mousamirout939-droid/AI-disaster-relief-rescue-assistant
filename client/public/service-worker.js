/**
 * Minimal offline-support service worker: caches the app shell so the UI
 * still loads (from cache) when the network is unavailable. API calls are
 * left to the network — cached GETs would show stale disaster data, which
 * is unsafe for an emergency app.
 */
const CACHE_NAME = 'disaster-relief-shell-v1';
const APP_SHELL = ['/', '/index.html', '/manifest.json', '/favicon.svg'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Never cache API calls — always hit the network for live disaster data.
  if (request.url.includes('/api/')) return;

  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).catch(() => caches.match('/index.html')))
  );
});
