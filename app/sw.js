// Service worker de jPique: permite abrir la app sin señal.
// construir.py completa la versión y la lista de archivos al armar la app.
const CACHE = "myv-fe33efd";
const ARCHIVOS = ["./", "index.html", "manifest.webmanifest", "anuncio.json", "icono-192.png", "icono-512.png", "icono-apple.png", "anuncio-elsenuelo.png", "fotos/anisotremus-scapularis-1.jpg", "fotos/anisotremus-scapularis-2.jpg", "fotos/anisotremus-scapularis-3.jpg", "fotos/basilichthys-australis-1.jpg", "fotos/basilichthys-australis-2.jpg", "fotos/callorhinchus-callorynchus-1.jpg", "fotos/callorhinchus-callorynchus-2.jpg", "fotos/cheilodactylus-variegatus-1.jpg", "fotos/cheilodactylus-variegatus-2.jpg", "fotos/cheilodactylus-variegatus-3.jpg", "fotos/cheilodactylus-variegatus-4.jpg", "fotos/cilus-gilberti-1.jpg", "fotos/cilus-gilberti-2.jpg", "fotos/cilus-gilberti-3.jpg", "fotos/cilus-gilberti-4.jpg", "fotos/girella-laevifrons-1.jpg", "fotos/graus-nigra-1.jpg", "fotos/merluccius-gayi-1.jpg", "fotos/merluccius-gayi-2.jpg", "fotos/merluccius-gayi-3.jpg", "fotos/mustelus-whitneyi-1.jpg", "fotos/odontesthes-bonariensis-1.jpg", "fotos/odontesthes-bonariensis-2.jpg", "fotos/odontesthes-bonariensis-3.jpg", "fotos/odontesthes-bonariensis-4.jpg", "fotos/oncorhynchus-mykiss-1.jpg", "fotos/oncorhynchus-mykiss-2.jpg", "fotos/oncorhynchus-mykiss-3.jpg", "fotos/oncorhynchus-mykiss-4.jpg", "fotos/paralichthys-adspersus-1.jpg", "fotos/paralichthys-adspersus-2.jpg", "fotos/paralichthys-adspersus-3.jpg", "fotos/paralichthys-microps-1.jpg", "fotos/percichthys-trucha-1.jpg", "fotos/percichthys-trucha-2.jpg", "fotos/percichthys-trucha-3.jpg", "fotos/percichthys-trucha-4.jpg", "fotos/pinguipes-chilensis-1.jpg", "fotos/pinguipes-chilensis-2.jpg", "fotos/salmo-trutta-1.jpg", "fotos/salmo-trutta-2.jpg", "fotos/salmo-trutta-3.jpg", "fotos/salmo-trutta-4.jpg", "fotos/sarda-chiliensis-1.jpg", "fotos/sarda-chiliensis-2.jpg", "fotos/sarda-chiliensis-3.jpg", "fotos/sarda-chiliensis-4.jpg", "fotos/sciaena-deliciosa-1.jpg", "fotos/sciaena-deliciosa-2.jpg", "fotos/sciaena-deliciosa-3.jpg", "fotos/semicossyphus-darwini-1.jpg", "fotos/semicossyphus-darwini-2.jpg", "fotos/semicossyphus-darwini-3.jpg", "fotos/semicossyphus-darwini-4.jpg", "fotos/seriola-lalandi-1.jpg", "fotos/seriola-lalandi-2.jpg", "fotos/seriola-lalandi-3.jpg", "fotos/seriola-lalandi-4.jpg", "fotos/thyrsites-atun-1.jpg", "fotos/thyrsites-atun-2.jpg", "fotos/thyrsites-atun-3.jpg", "fotos/thyrsites-atun-4.jpg", "fotos/trachurus-murphyi-1.jpg", "fotos/trachurus-murphyi-s1.jpg", "fotos/trachurus-murphyi-s2.jpg", "fotos/trachurus-murphyi-s3.jpg"];

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
