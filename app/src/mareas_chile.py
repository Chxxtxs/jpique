"""Calcula las tablas de mareas de jPique para todo Chile con los mareógrafos del UHSLC.

Datos: University of Hawaii Sea Level Center (UHSLC), series horarias abiertas y gratuitas.
Cita: Caldwell, P. C., M. A. Merrifield, P. R. Thompson (2015), Sea level measured by tide gauges
from global oceans — the Joint Archive for Sea Level holdings (NCEI Accession 0019568), NOAA NCEI.

Para cada estación hace un análisis armónico (paquete utide) de sus últimos 3 años de datos y predice
las pleamares y bajamares hasta fines de 2028. Resultado: app/mareas.json (la app lo carga al abrir).

Uso:  pip install utide numpy   y luego   python mareas_chile.py
"""
import csv, io, json, os, time, urllib.request
from datetime import datetime, timedelta

import numpy as np
import utide

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "mareas.json")
BASE = "https://uhslc.soest.hawaii.edu/data/csv/"
# id UHSLC: (nombre, latitud, longitud, carpeta del archivo)
ESTACIONES = {
    83: ("Arica", -18.4667, -70.3333, "fast/hourly/h083.csv"),
    80: ("Antofagasta", -23.6533, -70.405, "fast/hourly/h080.csv"),
    88: ("Caldera", -27.0667, -70.8333, "fast/hourly/h088.csv"),
    81: ("Valparaíso", -33.0267, -71.6267, "fast/hourly/h081.csv"),
    684: ("Puerto Montt", -41.485, -72.9617, "fast/hourly/h684.csv"),
    287: ("Puerto Williams", -54.9333, -67.6167, "rqds/atlantic/hourly/h287a.csv"),
    21: ("Isla Juan Fernández", -33.6367, -78.83, "fast/hourly/h021.csv"),
    22: ("Isla de Pascua", -27.155, -109.4733, "fast/hourly/h022.csv"),
}
DESDE, HASTA = datetime(2026, 9, 1), datetime(2029, 1, 1)
EPOCA = datetime(1970, 1, 1)


def serie(ruta):
    req = urllib.request.Request(BASE + ruta, headers={"User-Agent": "jPique/1.0 (github.com/Chxxtxs/jpique)"})
    texto = urllib.request.urlopen(req, timeout=300).read().decode()
    t, h = [], []
    for y, m, d, hh, v in csv.reader(io.StringIO(texto)):
        v = int(v)
        if v > -32000:
            t.append(datetime(int(y), int(m), int(d), int(hh))); h.append(v / 10.0)  # mm -> cm
    t, h = np.array(t), np.array(h)
    corte = t[-1] - timedelta(days=3 * 365)
    return t[t >= corte], h[t >= corte]


def main():
    salida = {"generado": time.strftime("%Y-%m-%d"), "estaciones": {}}
    paso = timedelta(minutes=6)
    n = int((HASTA - DESDE) / paso)
    tp = np.array([DESDE + i * paso for i in range(n)])
    for sid, (nombre, lat, lon, ruta) in ESTACIONES.items():
        t, h = serie(ruta)
        coef = utide.solve(t, h, lat=lat, method="ols", conf_int="none", verbose=False, trend=False)
        hp = utide.reconstruct(tp, coef, verbose=False).h - coef.mean
        ext = []
        for i in range(1, n - 1):
            if (hp[i] > hp[i - 1] and hp[i] >= hp[i + 1]) or (hp[i] < hp[i - 1] and hp[i] <= hp[i + 1]):
                ext.append([int((tp[i] - EPOCA).total_seconds() // 60), round(float(hp[i]))])
        comp = {c: round(float(a), 1) for c, a in zip(coef.name, coef.A) if c in ("M2", "S2", "K1", "O1", "N2", "P1", "K2")}
        salida["estaciones"][str(sid)] = {"n": nombre, "lat": lat, "lon": lon, "datos": f"{t[0]:%Y-%m} a {t[-1]:%Y-%m}", "comp": comp, "ext": ext}
        print(f"{sid:>3} {nombre:<20} {len(t):>6} horas ({t[0]:%Y-%m} a {t[-1]:%Y-%m})  M2={comp.get('M2')} cm  S2={comp.get('S2')} cm  {len(ext)} extremos")
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, separators=(",", ":"))
    print("mareas.json:", round(os.path.getsize(SALIDA) / 1024), "KB")


if __name__ == "__main__":
    main()
