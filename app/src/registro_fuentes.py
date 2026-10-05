"""Genera FUENTES_Y_LICENCIAS.md: el registro de dónde sale cada dato de la app y con qué licencia.

Uso: python registro_fuentes.py   (vuelve a correrlo si cambian las fotos)
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "..", "..", "FUENTES_Y_LICENCIAS.md")
snap = json.load(open(os.path.join(AQUI, "snapshot.json"), encoding="utf-8"))


def autor(a):
    a = a.replace("(c) ", "").split(", some rights reserved")[0]
    a = a.rsplit(" (", 1)[0] if a.endswith(")") else a
    return a.strip() if a.strip() and a.strip() != "no rights reserved" else "Autor no indicado"


filas = []
for sci, fotos in sorted(snap["fotos"].items()):
    for f in fotos:
        lic = f["licencia"].upper().replace("CC-", "CC ") if "public" not in f["licencia"].lower() else "Dominio público"
        filas.append(f"| *{sci}* | `{f['archivo']}` | {autor(f['autor'])} | {lic} | [ver original]({f['fuente']}) |")

md = f"""# jPique: fuentes, licencias y costos

Registro de dónde sale cada dato de la app. Revisado el 5 de octubre de 2026.
**Costo total de mantener la app: $0**, incluso con un aviso de un auspiciador: todas las fuentes permiten uso comercial gratis.

## Datos

| Dato | Fuente | Licencia o condición | Costo |
|---|---|---|---|
| Vedas, tallas, cuotas y temporadas | [Sernapesca: Medidas de administración de pesca recreativa 2026-2027](https://www.sernapesca.cl/manuales_y_publicaciones/temporadas-de-pesca-recreativa-en-chile/) (versión del 11-09-2026) y resoluciones de [Subpesca](https://www.subpesca.cl/portal/normativa/Regulaciones-de-pesca-recreativa/) | Normas públicas. Se usan los datos, no el documento; los textos son propios y cada ficha cita la norma. | $0 |
| Viento y temperatura | [MET Norway Locationforecast](https://api.met.no/) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), uso comercial permitido. Crédito visible en la app. Hay que identificarse (User-Agent) en el script; si la app crece mucho, pide un intermediario con caché. | $0 |
| Olas (altura y periodo) | [NOAA WaveWatch III vía PacIOOS ERDDAP](https://pae-paha.pacioos.hawaii.edu/erddap/griddap/ww3_global.html) | «The data may be used and redistributed for free». Crédito visible en la app. | $0 |
| Mareas | Cálculo propio (análisis armónico, paquete utide) con 8 mareógrafos del [UHSLC](https://uhslc.soest.hawaii.edu/): Arica (83), Antofagasta (80), Caldera (88), Valparaíso (81), Puerto Montt (684), Puerto Williams (287), Isla Juan Fernández (21) e Isla de Pascua (22) | Datos abiertos y gratuitos. Cita: Caldwell, P. C., M. A. Merrifield, P. R. Thompson (2015), *Sea level measured by tide gauges from global oceans — the Joint Archive for Sea Level holdings*, NOAA NCEI Accession 0019568. Predicción hasta fines de 2028 en `app/mareas.json` (regenerar con `mareas_chile.py`). Cada lugar usa su estación (por región; Ñuble a Los Ríos usan Valparaíso porque Puerto Montt tiene mareas mucho mayores). Aysén y Magallanes (salvo Puerto Williams) no tienen predicción. | $0 |
| Salida y puesta de sol, estado del mar | Cálculo propio | Fórmulas astronómicas públicas. | $0 |
| Fase lunar, posición de la luna y actividad de peces | Cálculo propio con fórmulas astronómicas públicas (Meeus) | Sin licencia de terceros. | $0 |
| Licencia de pesca (precio y requisitos) | [pescarecreativa.sernapesca.cl](https://pescarecreativa.sernapesca.cl) y Ley 20.256 | Información pública. | $0 |
| Tips de pesca (pestaña Tips) | Resumen propio de las [fichas ícticas de Sernapesca](https://www.sernapesca.cl/app/uploads/2023/11/fichas_icticas_de_especies_para_la_pesca_recreativa_parte_2_especies_dulceacuicolas.pdf), la [guía de The Nature Conservancy](https://www.nature.org/content/dam/tnc/nature/en/documents/TNC_CHILE_LIBRILLO_PECES_LITORALES.pdf) y guías de Stella Maris, Outdoor Online, D Multisport, Micky Baits, Pesca-Chile, Aipeces y otras (enlazadas en cada tip) | Hechos resumidos con palabras propias, sin copiar textos; cada tip enlaza su fuente. Lo legal (aparejos, carnada viva) sale de las normas oficiales. | $0 |
| Lugares de pesca (81, de Arica a Magallanes) | Coordenadas aproximadas (±2 km) cargadas a mano en `app/src/lugares.py` | Propias. | $0 |
| Capturas, carpetas y licencia del usuario | Las sube cada persona | Se guardan solo en su celular; la app no las envía a ningún servidor. | $0 |

## Software de terceros

| Componente | Uso | Licencia | Costo |
|---|---|---|---|
| [pdf.js](https://github.com/mozilla/pdf.js) 3.11.174 | Leer el PDF de la licencia | Apache 2.0 | $0 |
| [JSZip](https://stuk.github.io/jszip/) 3.10.1 | Copias de seguridad y descargar carpetas | MIT | $0 |
| Familjen Grotesk, IBM Plex Sans, IBM Plex Mono ([Google Fonts](https://fonts.google.com/)) | Tipografías | SIL Open Font License | $0 |

## Publicación

| Qué | Opción gratis |
|---|---|
| Alojar la app (https) | GitHub Pages, Cloudflare Pages o Netlify, plan gratis |
| Instalar en el celular | Desde el navegador: Android (Chrome, «Instalar app») e iPhone (Safari, «Agregar a inicio»). Sin Google Play (USD 25) ni App Store (USD 99 al año). |

## Fuentes que NO se usan

| Fuente | Motivo |
|---|---|
| tablademareas.com | Todos los derechos reservados, sin API pública. |
| SHOA (tabla oficial de mareas) | Se vende. Opcional a futuro, con convenio. |
| Open-Meteo | Gratis solo sin avisos ni cobros; con un aviso habría que pagar el plan comercial. |
| WorldTides, Stormglass | Pagados. |
| Fotos de Google, de otras apps o con licencia «NC» | No permiten este uso. |

## Fotos de especies ({len(filas)})

Todas permiten uso comercial. En la app cada foto muestra autor, licencia (con enlace) y fuente, y se indica que el tamaño fue reducido.
Las CC BY-SA obligan a que una versión editada (por ejemplo, con flechas) lleve la misma licencia.

| Especie | Archivo | Autor | Licencia | Fuente |
|---|---|---|---|---|
""" + "\n".join(filas) + """

## Condiciones para que siga siendo gratis

1. Mantener visibles los créditos de MET Norway, NOAA/PacIOOS, UHSLC y de cada foto.
2. Revisar la planilla de Sernapesca una vez al mes y actualizar la fecha de verificación.
3. Antes de 2030, volver a correr `mareas_valparaiso.py` para extender la tabla de mareas.
4. El aviso (auspiciador) se configura en `app/anuncio.json`.
"""
open(SALIDA, "w", encoding="utf-8").write(md)
print("Listo:", os.path.abspath(SALIDA), "·", len(filas), "fotos")
