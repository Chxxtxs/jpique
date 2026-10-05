// Service worker de jPique: permite abrir la app sin señal.
// construir.py completa la versión y la lista de archivos al armar la app.
const CACHE = "myv-__VERSION__";
const ARCHIVOS = __ARCHIVOS__;

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ARCHIVOS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith("myv-") && k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // version.json nunca se guarda: siempre se pregunta al servidor si hay una versión nueva
  if (url.origin === self.location.origin && url.pathname.endsWith("version.json")) {
    e.respondWith(fetch(req, { cache: "no-store" }));
    return;
  }

  // Pronóstico: primero internet; sin señal, la última respuesta guardada
  if (url.hostname === "api.met.no" || url.hostname.endsWith("pacioos.hawaii.edu") || url.pathname.endsWith("anuncio.json")) {
    e.respondWith(fetch(req).then((r) => { const copia = r.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); return r; }).catch(() => caches.match(req)));
    return;
  }
  // Librerías (pdf.js, JSZip) y tipografías: se guardan la primera vez que se usan
  if (url.hostname === "cdnjs.cloudflare.com" || url.hostname.endsWith("googleapis.com") || url.hostname.endsWith("gstatic.com")) {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((r) => { const copia = r.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); return r; })));
    return;
  }
  // La página: primero internet para recibir la versión nueva; sin señal, la guardada
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then((r) => { const copia = r.clone(); caches.open(CACHE).then((c) => c.put("index.html", copia)); return r; })
      .catch(() => caches.match("index.html")));
    return;
  }
  // Fotos e íconos: lo guardado al tiro y se actualiza en segundo plano
  if (url.origin === self.location.origin) {
    e.respondWith(caches.match(req, { ignoreSearch: true }).then((hit) => {
      const red = fetch(req).then((r) => { if (r.ok) { const copia = r.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); } return r; }).catch(() => hit);
      return hit || red;
    }));
  }
});
