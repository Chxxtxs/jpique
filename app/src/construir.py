"""Arma app/index.html a partir de la plantilla, el catálogo de lugares y el pronóstico guardado.

Uso:
  python construir.py            -> descarga pronóstico nuevo (MET Norway y NOAA) y arma index.html
  python construir.py --offline  -> solo arma index.html con snapshot.json existente

Antes hay que tener app/mareas.json (se genera con mareas_chile.py) y las fotos en app/fotos.
"""
import hashlib, json, math, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

from lugares import LUGARES, REGIONES, TZ_LUGAR, TZ_REGION

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
SNAP = os.path.join(AQUI, "snapshot.json")
PLANTILLA = os.path.join(AQUI, "index.template.html")
SALIDA = os.path.join(RAIZ, "index.html")

# Fuentes gratuitas con uso comercial permitido (ver FUENTES_Y_LICENCIAS.md)
MET = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat:.4f}&lon={lon:.4f}"
OLAS = "https://pae-paha.pacioos.hawaii.edu/erddap/griddap/ww3_global.json?"
AGENTE = {"User-Agent": "jPique/1.0 (app de pesca recreativa en Chile; github.com/Chxxtxs/jpique)"}  # MET Norway exige identificarse

# Mareógrafos del UHSLC (id: latitud, longitud). Los mismos de mareas_chile.py
ESTACIONES = {83: (-18.4667, -70.3333), 80: (-23.6533, -70.405), 88: (-27.0667, -70.8333), 81: (-33.0267, -71.6267),
              684: (-41.485, -72.9617), 287: (-54.9333, -67.6167), 21: (-33.6367, -78.83), 22: (-27.155, -109.4733)}
# Estación de marea por región. Entre Ñuble y Los Ríos se usa Valparaíso porque Puerto Montt tiene mareas mucho mayores.
EST_REGION = {"Arica y Parinacota": 83, "Tarapacá": 83, "Antofagasta": 80, "Atacama": 88, "Ñuble": 81, "Biobío": 81,
              "La Araucanía": 81, "Los Ríos": 81, "Los Lagos": 684}
EST_LUGAR = {"juanfernandez": 21, "hangaroa": 22, "williams": 287}
SIN_MAREA = {"Aysén", "Magallanes"}  # canales y fiordos: sin mareógrafo confiable (salvo Puerto Williams)
SIN_OLAS = {"Aysén", "Magallanes"}  # el modelo (celdas de 55 km) marca casi 0 m en canales y fiordos: sería un dato falso
RADIO_OLAS_KM = 90                   # más lejos que esto, el modelo de olas no representa el lugar (canales, fiordos)


def km(a, b):
    r = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def estacion(lugar):
    """Mareógrafo para un lugar de mar: (id, distancia en km) o (None, None)."""
    id_, _, region, tipo, lat, lon = lugar
    if tipo not in ("orilla", "roquerío"):
        return None, None
    if id_ in EST_LUGAR:
        e = EST_LUGAR[id_]
    elif region in EST_REGION:
        e = EST_REGION[region]
    elif region in SIN_MAREA:
        return None, None
    else:  # Coquimbo a Maule: el más cercano entre Caldera y Valparaíso
        e = min((88, 81), key=lambda s: km((lat, lon), ESTACIONES[s]))
    return e, round(km((lat, lon), ESTACIONES[e]))


def ms(iso):
    return int(datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp() * 1000)


def get_ua(url, timeout=90, intentos=4):
    """Descarga JSON con reintentos: los servidores gratuitos a veces tardan o responden 503."""
    ultimo = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers=AGENTE)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            ultimo = e
            time.sleep(2 + 3 * i)
    raise ultimo


def celdas_oceano():
    """Celdas de 0,5° del modelo de olas que tienen mar (no son tierra ni canal): lista de (lat, lon_este)."""
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%dT12:00:00Z")
    celdas = []
    for lat0, lat1, lon0, lon1 in ((-56, -17, 276, 295), (-29, -26, 248, 253)):
        sel = f"[({hoy})][(0.0)][({lat0}):({lat1})][({lon0}):({lon1})]"
        filas = get_ua(OLAS + urllib.parse.quote("Thgt" + sel), 120)["table"]["rows"]
        celdas += [(r[2], r[3]) for r in filas if r[4] is not None]
    return celdas


def celda_para(lugar, celdas):
    id_, _, _, tipo, lat, lon = lugar
    if tipo not in ("orilla", "roquerío") or not celdas:
        return None
    lon_e = lon % 360
    mejor = min(celdas, key=lambda c: km((lat, lon), (c[0], c[1] - 360 if c[1] > 180 else c[1])))
    d = km((lat, lon), (mejor[0], mejor[1] - 360 if mejor[1] > 180 else mejor[1]))
    return [mejor[0], mejor[1]] if d <= RADIO_OLAS_KM else None


def armar_lugares(snap, celdas):
    previos = {s["id"]: s for s in snap.get("spots", [])}
    out = []
    for lug in LUGARES:
        id_, nombre, region, tipo, lat, lon = lug
        est, d = estacion(lug)
        celda = celda_para(lug, celdas) if celdas else (previos.get(id_) or {}).get("celda")
        if region in SIN_OLAS:
            celda = None
        out.append({"id": id_, "nombre": nombre, "region": region, "tipo": tipo, "lat": lat, "lon": lon,
                    "tz": TZ_LUGAR.get(id_) or TZ_REGION.get(region) or "America/Santiago", "est": est, "estKm": d, "celda": celda})
    return out


def compacto(base, tiempos, **series):
    """Serie guardada en poco espacio: minutos desde una base y valores redondeados."""
    return {"b": base, "t": [round((t - base) / 60000) for t in tiempos], **series}


def actualizar(snap):
    try:
        celdas = celdas_oceano()
        print("celdas de mar:", len(celdas))
    except Exception as e:
        celdas = []
        print("No se pudieron leer las celdas del modelo de olas:", e)
    snap["spots"] = armar_lugares(snap, celdas)
    crudo = snap.get("crudo", {})
    olas = snap.get("olas", {})
    desde = (datetime.now(timezone.utc) - timedelta(hours=30)).strftime("%Y-%m-%dT%H:00:00Z")
    nuevas = {}
    fallos = 0
    for s in snap["spots"]:
        try:
            ts = get_ua(MET.format(lat=s["lat"], lon=s["lon"]))["properties"]["timeseries"]
            d = [x["data"]["instant"]["details"] for x in ts]
            t = [ms(x["time"]) for x in ts]
            r1 = lambda v, n: None if v is None else round(v, n)
            nuevas[s["id"]] = compacto(t[0], t, v=[r1(x.get("wind_speed"), 1) for x in d], d=[r1(x.get("wind_from_direction"), 0) for x in d],
                                       c=[r1(x.get("air_temperature"), 1) for x in d])
        except Exception as e:
            fallos += 1
            print("  sin pronóstico nuevo para", s["id"], "->", e)
        time.sleep(0.25)
    crudo.update(nuevas)
    nuevas_olas = {}
    for c in {tuple(s["celda"]) for s in snap["spots"] if s.get("celda")}:
        clave = f"{c[0]:g},{c[1]:g}"  # igual que celda.join(",") en la app
        try:
            sel = f"[({desde}):1:(last)][(0.0)][({c[0]})][({c[1]})]"
            rows = get_ua(OLAS + urllib.parse.quote(f"Thgt{sel},Tper{sel}"))["table"]["rows"]
            t = [ms(r[0]) for r in rows]
            nuevas_olas[clave] = compacto(t[0], t, hs=[None if r[4] is None else round(r[4], 2) for r in rows], tp=[None if r[5] is None else round(r[5], 1) for r in rows])
        except Exception as e:
            fallos += 1
            print("  sin olas nuevas para", clave, "->", e)
        time.sleep(0.25)
    olas.update(nuevas_olas)
    en_uso = {f"{s['celda'][0]:g},{s['celda'][1]:g}" for s in snap["spots"] if s.get("celda")}
    ids = {s["id"] for s in snap["spots"]}
    snap["crudo"] = {k: v for k, v in crudo.items() if k in ids and "b" in v}  # descarta el formato antiguo
    snap["olas"] = {k: v for k, v in olas.items() if k in en_uso and "b" in v}
    snap["generado"] = time.strftime("%Y-%m-%dT%H:%M")
    print(f"pronóstico: {len(nuevas)} lugares y {len(nuevas_olas)} celdas de olas nuevos, {fallos} fallos")


def main():
    with open(SNAP, encoding="utf-8") as f:
        snap = json.load(f)
    snap.pop("mareas", None)  # las mareas ahora viven en app/mareas.json
    if "--offline" in sys.argv:
        snap["spots"] = armar_lugares(snap, [])  # mantiene las celdas ya calculadas
    else:
        actualizar(snap)
    with open(SNAP, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, separators=(",", ":"))
    snap["regiones"] = REGIONES
    fotos = sorted("fotos/" + n for n in os.listdir(os.path.join(RAIZ, "fotos")))
    extras = sorted(n for n in os.listdir(RAIZ) if n.startswith("anuncio-"))  # logos de auspiciadores
    archivos = ["./", "index.html", "manifest.webmanifest", "anuncio.json", "mareas.json", "icono-192.png", "icono-512.png", "icono-apple.png"] + extras + fotos
    with open(PLANTILLA, encoding="utf-8") as f:
        plantilla = f.read()
    with open(os.path.join(AQUI, "sw.template.js"), encoding="utf-8") as f:
        sw_plantilla = f.read()
    # Versión de la app: cambia solo cuando cambia el código, los lugares, el aviso o las fotos (no con el pronóstico diario)
    huella = hashlib.sha1()
    for parte in (plantilla, sw_plantilla, json.dumps(archivos), json.dumps(snap.get("fotos", {}), sort_keys=True),
                  json.dumps([{k: v for k, v in s.items() if k != "celda"} for s in snap["spots"]], sort_keys=True)):
        huella.update(parte.encode("utf-8"))
    for n in ["anuncio.json", "manifest.webmanifest", "mareas.json"] + extras:
        huella.update(open(os.path.join(RAIZ, n), "rb").read())
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
    # Service worker: guarda la app, los íconos, las mareas y las fotos de especies para usarla sin señal
    sw = sw_plantilla.replace("__VERSION__", version).replace("__ARCHIVOS__", json.dumps(archivos, ensure_ascii=False))
    with open(os.path.join(RAIZ, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    # version.json: el botón «Buscar actualización» de la app lo compara con su propia versión
    with open(os.path.join(RAIZ, "version.json"), "w", encoding="utf-8") as f:
        json.dump({"version": version, "fecha": time.strftime("%Y-%m-%d"), "pronostico": snap["generado"]}, f)
    # Versión sin cabecera para publicar como Artifact (el publicador agrega su propio esqueleto)
    with open(os.path.join(RAIZ, "publicar.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html listo · versión", version, "·", len(snap["spots"]), "lugares · pronóstico del", snap["generado"],
          "·", round(len(completo) / 1024), "KB")


if __name__ == "__main__":
    main()
