"""Arma app/index.html a partir de la plantilla y del pronóstico guardado.

Uso:
  python construir.py            -> descarga pronóstico nuevo (MET Norway y NOAA) y arma index.html
  python construir.py --offline  -> solo arma index.html con snapshot.json existente
"""
import hashlib, json, os, sys, time, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(AQUI, "snapshot.json")
PLANTILLA = os.path.join(AQUI, "index.template.html")
SALIDA = os.path.join(AQUI, "..", "index.html")


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())


# Fuentes gratuitas con uso comercial permitido (ver FUENTES_Y_LICENCIAS.md)
MET = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat:.4f}&lon={lon:.4f}"
OLAS = "https://pae-paha.pacioos.hawaii.edu/erddap/griddap/ww3_global.json?"
AGENTE = {"User-Agent": "jPique/1.0 (app de pesca recreativa, Chile)"}  # MET Norway exige identificarse
CELDA_OLAS = {"papudo": (-32.5, 288.5), "quintero": (-33, 288), "concon": (-33, 288), "valparaiso": (-33, 288), "algarrobo": (-33.5, 288),
              "cartagena": (-33.5, 288), "llolleo": (-33.5, 288), "navidad": (-34, 288), "pichilemu": (-34.5, 287.5), "bucalemu": (-34.5, 287.5),
              "constitucion": (-35, 287.5), "pelluhue": (-36, 287)}


def ms(iso):
    from datetime import datetime
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


def get_ua(url):
    req = urllib.request.Request(url, headers=AGENTE)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def actualizar(snap):
    from datetime import datetime, timedelta, timezone
    crudo, olas_cache = {}, {}
    desde = (datetime.now(timezone.utc) - timedelta(hours=30)).strftime("%Y-%m-%dT%H:00:00Z")
    for s in snap["spots"]:
        ts = get_ua(MET.format(lat=s["lat"], lon=s["lon"]))["properties"]["timeseries"]
        d = [x["data"]["instant"]["details"] for x in ts]
        c = {"tiempo": {"t": [ms(x["time"]) for x in ts], "v": [x.get("wind_speed") for x in d],
                        "d": [x.get("wind_from_direction") for x in d], "c": [x.get("air_temperature") for x in d]}, "olas": None}
        celda = CELDA_OLAS.get(s["id"])
        if celda:
            if celda not in olas_cache:
                sel = f"[({desde}):1:(last)][(0.0)][({celda[0]})][({celda[1]})]"
                rows = get_ua(OLAS + urllib.parse.quote(f"Thgt{sel},Tper{sel}"))["table"]["rows"]
                olas_cache[celda] = {"t": [ms(r[0]) for r in rows], "hs": [r[4] for r in rows], "tp": [r[5] for r in rows]}
            c["olas"] = olas_cache[celda]
        crudo[s["id"]] = c
        time.sleep(0.3)
    snap["crudo"] = crudo
    snap.pop("marine", None); snap.pop("weather", None)
    snap["generado"] = time.strftime("%Y-%m-%dT%H:%M")


def main():
    with open(SNAP, encoding="utf-8") as f:
        snap = json.load(f)
    # Mareas calculadas con el mareógrafo de Valparaíso (generar con mareas_valparaiso.py)
    snap["mareas"] = json.load(open(os.path.join(AQUI, "mareas.json"), encoding="utf-8"))
    if "--offline" not in sys.argv:
        actualizar(snap)
        with open(SNAP, "w", encoding="utf-8") as f:
            json.dump(snap, f, ensure_ascii=False, separators=(",", ":"))
    raiz = os.path.join(AQUI, "..")
    fotos = sorted("fotos/" + n for n in os.listdir(os.path.join(raiz, "fotos")))
    extras = sorted(n for n in os.listdir(raiz) if n.startswith("anuncio-"))  # logos de auspiciadores
    archivos = ["./", "index.html", "manifest.webmanifest", "anuncio.json", "icono-192.png", "icono-512.png", "icono-apple.png"] + extras + fotos
    with open(PLANTILLA, encoding="utf-8") as f:
        plantilla = f.read()
    with open(os.path.join(AQUI, "sw.template.js"), encoding="utf-8") as f:
        sw_plantilla = f.read()
    # Versión de la app: cambia solo cuando cambia el código, el aviso o las fotos (no con el pronóstico diario)
    huella = hashlib.sha1()
    for parte in (plantilla, sw_plantilla, json.dumps(archivos), json.dumps(snap.get("fotos", {}), sort_keys=True)):
        huella.update(parte.encode("utf-8"))
    for n in ["anuncio.json", "manifest.webmanifest"] + extras:
        huella.update(open(os.path.join(raiz, n), "rb").read())
    version = huella.hexdigest()[:7]
    datos = json.dumps(snap, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = plantilla.replace("__SNAPSHOT__", datos).replace("__APP_VERSION__", version)
    cabecera = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                '<meta name="theme-color" content="#0d1418">\n'
                '<meta name="mobile-web-app-capable" content="yes">\n'
                '<meta name="apple-mobile-web-app-capable" content="yes">\n'
                '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
                '<meta name="apple-mobile-web-app-title" content="jPique">\n'
                '<link rel="manifest" href="manifest.webmanifest">\n'
                '<link rel="icon" href="icono-192.png">\n'
                '<link rel="apple-touch-icon" href="icono-apple.png">\n')
    completo = cabecera + html + "\n</html>\n"
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(completo)
    # Service worker: guarda la app, los íconos y las fotos de especies para usarla sin señal
    sw = sw_plantilla.replace("__VERSION__", version).replace("__ARCHIVOS__", json.dumps(archivos, ensure_ascii=False))
    with open(os.path.join(raiz, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    # version.json: el botón «Buscar actualización» de la app lo compara con su propia versión
    with open(os.path.join(raiz, "version.json"), "w", encoding="utf-8") as f:
        json.dump({"version": version, "fecha": time.strftime("%Y-%m-%d"), "pronostico": snap["generado"]}, f)
    # Versión sin cabecera para publicar como Artifact (el publicador agrega su propio esqueleto)
    with open(os.path.join(AQUI, "..", "publicar.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html listo · versión", version, "· pronóstico del", snap["generado"])


if __name__ == "__main__":
    main()
