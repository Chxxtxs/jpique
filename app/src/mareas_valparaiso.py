"""Calcula la tabla de mareas de la app a partir del mareógrafo de Valparaíso (UHSLC, estación 081).

Datos: University of Hawaii Sea Level Center, hourly "fast delivery" (abiertos y gratuitos).
Cita: Caldwell, P. C., M. A. Merrifield, P. R. Thompson (2015), Sea level measured by tide gauges
from global oceans — the Joint Archive for Sea Level holdings (NCEI Accession 0019568), NOAA NCEI.

Hace un análisis armónico (paquete utide) de los últimos 3 años y predice pleamares y bajamares
hasta fines de 2029. Resultado: mareas.json (minutos desde 1970 UTC y altura en cm sobre el nivel medio).

Uso: pip install utide numpy   y luego   python mareas_valparaiso.py
"""
import csv, io, json, os, urllib.request
from datetime import datetime, timedelta, timezone

import numpy as np
import utide

AQUI = os.path.dirname(os.path.abspath(__file__))
URL = "https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h081.csv"
DESDE_ANALISIS = datetime(2023, 8, 1)
PREDICCION = (datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2030, 1, 1, tzinfo=timezone.utc))


def leer():
    with urllib.request.urlopen(URL, timeout=120) as r:
        texto = r.read().decode()
    t, h = [], []
    for y, m, d, hh, v in csv.reader(io.StringIO(texto)):
        v = int(v)
        if v <= -32000:
            continue
        fecha = datetime(int(y), int(m), int(d), int(hh))
        if fecha >= DESDE_ANALISIS:
            t.append(fecha); h.append(v / 10.0)  # mm -> cm
    return np.array(t), np.array(h)


def main():
    t, h = leer()
    print(f"{len(t)} horas válidas, de {t[0]} a {t[-1]}")
    coef = utide.solve(t, h, lat=-33.03, method="ols", conf_int="none", verbose=False, trend=False)
    # Predicción cada 6 minutos para ubicar bien pleamares y bajamares
    paso = timedelta(minutes=6)
    n = int((PREDICCION[1] - PREDICCION[0]) / paso)
    tp = np.array([PREDICCION[0].replace(tzinfo=None) + i * paso for i in range(n)])
    hp = utide.reconstruct(tp, coef, verbose=False).h - coef.mean
    ext = []
    for i in range(1, n - 1):
        if (hp[i] > hp[i - 1] and hp[i] >= hp[i + 1]) or (hp[i] < hp[i - 1] and hp[i] <= hp[i + 1]):
            mins = int((tp[i] - datetime(1970, 1, 1)).total_seconds() // 60)
            ext.append([mins, round(float(hp[i]))])
    principales = sorted(zip(coef.name, coef.A), key=lambda x: -x[1])[:8]
    salida = {"estacion": "Valparaíso (UHSLC 081)", "datos_hasta": str(t[-1].date()),
              "referencia": "cm sobre el nivel medio del mar", "extremos": ext,
              # Amplitudes en cm: la app las usa para el coeficiente de marea (mareas vivas y muertas medias)
              "componentes": {n: round(float(a), 1) for n, a in zip(coef.name, coef.A) if n in ("M2", "S2", "K1", "O1", "N2", "P1", "K2")}}
    json.dump(salida, open(os.path.join(AQUI, "mareas.json"), "w", encoding="utf-8"), separators=(",", ":"))
    print("Componentes principales (cm):", ", ".join(f"{n} {a:.1f}" for n, a in principales))
    print(f"{len(ext)} pleamares y bajamares guardadas en mareas.json")


if __name__ == "__main__":
    main()
