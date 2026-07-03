// Service Worker dla Narzędzi dla Nauczycieli
const CACHE_NAME = 'nauczyciel-tools-v5';

// Pliki do cache'owania przy instalacji (ścieżki względne dla GitHub Pages)
const STATIC_ASSETS = [
  './',
  './index.html',
  './styles-common.css',
  './scripts-common.js',
  './timer-kartkowka.html',
  './timer-egzamin.html',
  './progi-ocen.html',
  './losowanie-ucznia.html',
  './tabliczka-kolko-krzyzyk.html',
  './mapa-polski.html',
  './wyniki.html',
  './stworek.html',
  './termometr-emocji.html',
  './manifest.json',
  './icons/icon-192.png',
  './programowanie-robotow.html'
];

// Pliki które wymagają sieci (Firebase)
const NETWORK_ONLY = [
  'turniej-tabliczka.html'
];

// Instalacja - cache'uj statyczne zasoby
self.addEventListener('install', (event) => {
  console.log('[SW] Instalacja...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Cache\'owanie statycznych zasobów');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Instalacja zakończona');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW] Błąd instalacji:', error);
      })
  );
});

// Aktywacja - usuń stare cache
self.addEventListener('activate', (event) => {
  console.log('[SW] Aktywacja...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] Usuwanie starego cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Aktywacja zakończona');
        return self.clients.claim();
      })
  );
});

// Fetch - strategia Cache First z fallback do sieci
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Pomijaj requesty do innych domen (Firebase, GoatCounter, etc.)
  if (url.origin !== location.origin) {
    return;
  }

  // Network only dla turnieju (wymaga Firebase)
  if (NETWORK_ONLY.some(path => url.pathname.includes(path))) {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return new Response(
            '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body style="font-family:sans-serif;text-align:center;padding:50px;"><h1>Brak połączenia</h1><p>Turniej wymaga połączenia z internetem.</p><a href="./index.html">Wróć do strony głównej</a></body></html>',
            { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
          );
        })
    );
    return;
  }

  // Cache First dla pozostałych zasobów
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // Zwróć z cache, ale odśwież w tle
          event.waitUntil(
            fetch(event.request)
              .then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200) {
                  caches.open(CACHE_NAME)
                    .then((cache) => cache.put(event.request, networkResponse));
                }
              })
              .catch(() => {})
          );
          return cachedResponse;
        }

        // Nie ma w cache - pobierz z sieci
        return fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              const responseClone = networkResponse.clone();
              caches.open(CACHE_NAME)
                .then((cache) => cache.put(event.request, responseClone));
            }
            return networkResponse;
          })
          .catch(() => {
            // Offline fallback dla HTML
            if (event.request.headers.get('accept').includes('text/html')) {
              return caches.match('./index.html');
            }
          });
      })
  );
});

// Obsługa wiadomości (np. skip waiting)
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
