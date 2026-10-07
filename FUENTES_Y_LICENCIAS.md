# jPique: fuentes, licencias y costos

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
| [pdf.js](https://github.com/mozilla/pdf.js) 3.11.174 | Leer el PDF de la licencia (incluido en `app/lib/`) | Apache 2.0 | $0 |
| [JSZip](https://stuk.github.io/jszip/) 3.10.1 | Copias de seguridad y descargar carpetas (incluido en `app/lib/`) | MIT | $0 |
| Familjen Grotesk, IBM Plex Sans, IBM Plex Mono ([Google Fonts](https://fonts.google.com/)) | Tipografías (incluidas en `app/lib/fuentes/`, con su licencia en `app/lib/OFL.txt`) | SIL Open Font License 1.1 | $0 |
| [Capacitor](https://capacitorjs.com/) 8 y sus plugins App, Browser, Filesystem, Geolocation, Haptics y Share | App nativa para Android (`movil/`) | MIT | $0 |

## Publicación

| Qué | Opción gratis |
|---|---|
| Alojar la app (https) | GitHub Pages, Cloudflare Pages o Netlify, plan gratis |
| Instalar en el celular | Android: APK nativo compilado gratis en GitHub Actions y publicado en GitHub Releases. También desde el navegador: Android (Chrome, «Instalar app») e iPhone (Safari, «Agregar a inicio»). Sin Google Play (USD 25) ni App Store (USD 99 al año). |

## Fuentes que NO se usan

| Fuente | Motivo |
|---|---|
| tablademareas.com | Todos los derechos reservados, sin API pública. |
| SHOA (tabla oficial de mareas) | Se vende. Opcional a futuro, con convenio. |
| Open-Meteo | Gratis solo sin avisos ni cobros; con un aviso habría que pagar el plan comercial. |
| WorldTides, Stormglass | Pagados. |
| Fotos de Google, de otras apps o con licencia «NC» | No permiten este uso. |

## Fotos de especies (66)

Todas permiten uso comercial. En la app cada foto muestra autor, licencia (con enlace) y fuente, y se indica que el tamaño fue reducido.
Las CC BY-SA obligan a que una versión editada (por ejemplo, con flechas) lleve la misma licencia.

| Especie | Archivo | Autor | Licencia | Fuente |
|---|---|---|---|---|
| *Anisotremus scapularis* | `fotos/anisotremus-scapularis-1.jpg` | Savicale | CC BY-SA 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Ejemplar_de_chita_*Anisotrremus_scapularis*_en_Puerto_Quilca_(Per%C3%BA).jpg) |
| *Anisotremus scapularis* | `fotos/anisotremus-scapularis-2.jpg` | Charlotte Kirchner | CC BY 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Anisotremus_scapularis_556207461_(closeup).jpg) |
| *Anisotremus scapularis* | `fotos/anisotremus-scapularis-3.jpg` | Georgina Jones | CC BY-SA | [ver original](https://www.inaturalist.org/observations/240491796) |
| *Basilichthys australis* | `fotos/basilichthys-australis-1.jpg` | Katherin Solis-Lufí | CC BY | [ver original](https://www.inaturalist.org/observations/133424879) |
| *Basilichthys australis* | `fotos/basilichthys-australis-2.jpg` | Katherin Solis-Lufí | CC BY 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Basilichthys_australis_244002371.jpg) |
| *Callorhinchus callorynchus* | `fotos/callorhinchus-callorynchus-1.jpg` | Nicolas Olejnik | CC BY | [ver original](https://www.inaturalist.org/photos/1127037) |
| *Callorhinchus callorynchus* | `fotos/callorhinchus-callorynchus-2.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/159365872) |
| *Cheilodactylus variegatus* | `fotos/cheilodactylus-variegatus-1.jpg` | rguzman@urp.edu.pe | CC BY 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Chaylodactylus_variegatus.jpg) |
| *Cheilodactylus variegatus* | `fotos/cheilodactylus-variegatus-2.jpg` | cstobie | CC BY | [ver original](https://www.inaturalist.org/photos/18713299) |
| *Cheilodactylus variegatus* | `fotos/cheilodactylus-variegatus-3.jpg` | Kai Murphy | CC BY | [ver original](https://www.inaturalist.org/observations/306296307) |
| *Cheilodactylus variegatus* | `fotos/cheilodactylus-variegatus-4.jpg` | Juan A. Malo de Molina | CC BY-SA 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Pintadilla_-_Cheilodactylus_variegatus-_JMM-Ancon-20160709.jpg) |
| *Cilus gilberti* | `fotos/cilus-gilberti-1.jpg` | ProzaCL | CC BY-SA 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Corvina.jpg) |
| *Cilus gilberti* | `fotos/cilus-gilberti-2.jpg` | Antonio W. Salas | CC BY | [ver original](https://www.inaturalist.org/observations/55469586) |
| *Cilus gilberti* | `fotos/cilus-gilberti-3.jpg` | cstobie | CC BY | [ver original](https://www.inaturalist.org/observations/106120330) |
| *Cilus gilberti* | `fotos/cilus-gilberti-4.jpg` | Nicolas Olejnik | CC BY | [ver original](https://www.inaturalist.org/observations/38489270) |
| *Girella laevifrons* | `fotos/girella-laevifrons-1.jpg` | cstobie | CC BY | [ver original](https://www.inaturalist.org/photos/18415730) |
| *Graus nigra* | `fotos/graus-nigra-1.jpg` | Lawenai | CC BY-SA 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Vieja_o_Mulata_(Graus_Nigra).JPG) |
| *Merluccius gayi* | `fotos/merluccius-gayi-1.jpg` | Lycaon.cl | CC BY-SA 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Merluza.jpg) |
| *Merluccius gayi* | `fotos/merluccius-gayi-2.jpg` | Paul Louis Oudart (1796–1860) after Claudio Gay (1800-1873) prinx, Christophe Annedouche (1803-1866) sc | Dominio público | [ver original](https://commons.wikimedia.org/wiki/File:Merluccius_gayi.jpg) |
| *Merluccius gayi* | `fotos/merluccius-gayi-3.jpg` | Nelson Balcar | CC BY | [ver original](https://www.inaturalist.org/observations/193008665) |
| *Mustelus whitneyi* | `fotos/mustelus-whitneyi-1.jpg` | D Ross Robertson | Dominio público | [ver original](https://commons.wikimedia.org/wiki/File:Mustelus_whitneyi_SI.jpg) |
| *Odontesthes bonariensis* | `fotos/odontesthes-bonariensis-1.jpg` | no rights reserved, uploaded by Hugo Hulsberg | CC0 | [ver original](https://www.inaturalist.org/photos/104854137) |
| *Odontesthes bonariensis* | `fotos/odontesthes-bonariensis-2.jpg` | RAP | CC BY | [ver original](https://www.inaturalist.org/observations/158116820) |
| *Odontesthes bonariensis* | `fotos/odontesthes-bonariensis-3.jpg` | Martín Acosta Albarracín | CC BY | [ver original](https://www.inaturalist.org/photos/137496761) |
| *Odontesthes bonariensis* | `fotos/odontesthes-bonariensis-4.jpg` | no rights reserved, uploaded by Manuel Roncal | CC0 | [ver original](https://www.inaturalist.org/photos/125827433) |
| *Oncorhynchus mykiss* | `fotos/oncorhynchus-mykiss-1.jpg` | Bruce Deagle | CC BY | [ver original](https://www.inaturalist.org/photos/127663820) |
| *Oncorhynchus mykiss* | `fotos/oncorhynchus-mykiss-2.jpg` | Damien Mullin | CC BY | [ver original](https://www.inaturalist.org/observations/105230696) |
| *Oncorhynchus mykiss* | `fotos/oncorhynchus-mykiss-3.jpg` | mnauky | CC BY | [ver original](https://www.inaturalist.org/observations/251662395) |
| *Oncorhynchus mykiss* | `fotos/oncorhynchus-mykiss-4.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/2714093) |
| *Paralichthys adspersus* | `fotos/paralichthys-adspersus-1.jpg` | Daniel Ore Villalba | CC BY 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Fine_flounder.jpg) |
| *Paralichthys adspersus* | `fotos/paralichthys-adspersus-2.jpg` | Ben Lyle Bedard | CC BY | [ver original](https://www.inaturalist.org/observations/192397341) |
| *Paralichthys adspersus* | `fotos/paralichthys-adspersus-3.jpg` | Ben Lyle Bedard | CC BY | [ver original](https://www.inaturalist.org/observations/173828139) |
| *Paralichthys microps* | `fotos/paralichthys-microps-1.jpg` | Lycaon.cl | CC BY-SA 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Lenguado_ojos_chicos.jpg) |
| *Percichthys trucha* | `fotos/percichthys-trucha-1.jpg` | Pablo Reyes Lobao-Tello | CC BY 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Percichthys_trucha.png) |
| *Percichthys trucha* | `fotos/percichthys-trucha-2.jpg` | Jc hernaiz | CC BY-SA 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Perca_trucha_(Percichthys_trucha).JPG) |
| *Percichthys trucha* | `fotos/percichthys-trucha-3.jpg` | Pablo Reyes Lobao-Tello | CC BY 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Percichthys_trucha_juvenile.png) |
| *Percichthys trucha* | `fotos/percichthys-trucha-4.jpg` | Nicolas Olejnik | CC BY | [ver original](https://www.inaturalist.org/photos/1380559) |
| *Pinguipes chilensis* | `fotos/pinguipes-chilensis-1.jpg` | Edit-pi | CC0 | [ver original](https://commons.wikimedia.org/wiki/File:Pinguipes_chilensis.png) |
| *Pinguipes chilensis* | `fotos/pinguipes-chilensis-2.jpg` | Eric Schmidt | CC BY | [ver original](https://www.inaturalist.org/observations/265640718) |
| *Salmo trutta* | `fotos/salmo-trutta-1.jpg` | kirk gardner | CC BY | [ver original](https://www.inaturalist.org/photos/34847726) |
| *Salmo trutta* | `fotos/salmo-trutta-2.jpg` | Kagan Vainisi | CC BY | [ver original](https://www.inaturalist.org/observations/399785238) |
| *Salmo trutta* | `fotos/salmo-trutta-3.jpg` | Tim | CC BY-SA | [ver original](https://www.inaturalist.org/observations/63372593) |
| *Salmo trutta* | `fotos/salmo-trutta-4.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/197365179) |
| *Sarda chiliensis* | `fotos/sarda-chiliensis-1.jpg` | nmoorhatch | CC BY 4.0 | [ver original](https://commons.wikimedia.org/wiki/File:Sarda_chiliensis_61671693.jpg) |
| *Sarda chiliensis* | `fotos/sarda-chiliensis-2.jpg` | Ian Manning | CC BY | [ver original](https://www.inaturalist.org/observations/9804556) |
| *Sarda chiliensis* | `fotos/sarda-chiliensis-3.jpg` | Autor no indicado | Dominio público | [ver original](https://commons.wikimedia.org/wiki/File:Sachi_u0.gif) |
| *Sarda chiliensis* | `fotos/sarda-chiliensis-4.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/387672665) |
| *Sciaena deliciosa* | `fotos/sciaena-deliciosa-1.jpg` | cstobie, algunos derechos reservados (CC BY), subido por cstobie | CC BY | [ver original](https://www.inaturalist.org/photos/178210140) |
| *Sciaena deliciosa* | `fotos/sciaena-deliciosa-2.jpg` | United States National Museum; Smithsonian Institution; United States. Dept. of the Interior | Dominio público | [ver original](https://commons.wikimedia.org/wiki/File:Sciaena_deliciosa.jpg) |
| *Sciaena deliciosa* | `fotos/sciaena-deliciosa-3.jpg` | Antonio W. Salas | CC BY | [ver original](https://www.inaturalist.org/observations/55469629) |
| *Semicossyphus darwini* | `fotos/semicossyphus-darwini-1.jpg` | Yuri Hooker | CC BY-SA 3.0 | [ver original](https://commons.wikimedia.org/wiki/File:Semicossyphus_darwini_-_Peru.jpg) |
| *Semicossyphus darwini* | `fotos/semicossyphus-darwini-2.jpg` | Georgina Jones | CC BY-SA | [ver original](https://www.inaturalist.org/observations/239579210) |
| *Semicossyphus darwini* | `fotos/semicossyphus-darwini-3.jpg` | Leonard Jenyns,  Benjamin Waterhouse Hawkins | Dominio público | [ver original](https://commons.wikimedia.org/wiki/File:Semicossyphus_darwini.jpg) |
| *Semicossyphus darwini* | `fotos/semicossyphus-darwini-4.jpg` | The original uploader was Aquaimages at English Wikipedia. | CC BY-SA 2.5 | [ver original](https://commons.wikimedia.org/wiki/File:6070_aquaimages.jpg) |
| *Seriola lalandi* | `fotos/seriola-lalandi-1.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/330930768) |
| *Seriola lalandi* | `fotos/seriola-lalandi-2.jpg` | tobyyy | CC BY-SA | [ver original](https://www.inaturalist.org/observations/69447588) |
| *Seriola lalandi* | `fotos/seriola-lalandi-3.jpg` | Shaun Lee | CC BY | [ver original](https://www.inaturalist.org/observations/203498662) |
| *Seriola lalandi* | `fotos/seriola-lalandi-4.jpg` | Debra Baker | CC BY | [ver original](https://www.inaturalist.org/observations/261228182) |
| *Thyrsites atun* | `fotos/thyrsites-atun-1.jpg` | Jonas Sielenkämper | CC BY | [ver original](https://www.inaturalist.org/observations/262338721) |
| *Thyrsites atun* | `fotos/thyrsites-atun-2.jpg` | Michael Berardozzi | CC BY | [ver original](https://www.inaturalist.org/observations/173141337) |
| *Thyrsites atun* | `fotos/thyrsites-atun-3.jpg` | Steve Kerr | CC BY | [ver original](https://www.inaturalist.org/observations/10193793) |
| *Thyrsites atun* | `fotos/thyrsites-atun-4.jpg` | Michael Berardozzi | CC BY | [ver original](https://www.inaturalist.org/observations/173141337) |
| *Trachurus murphyi* | `fotos/trachurus-murphyi-s1.jpg` | Ed Bierman | CC BY 2.0 | [ver original](https://commons.wikimedia.org/wiki/File:Mackerel.jpg) |
| *Trachurus murphyi* | `fotos/trachurus-murphyi-s2.jpg` | Autor no indicado | CC0 | [ver original](https://www.inaturalist.org/observations/87453264) |
| *Trachurus murphyi* | `fotos/trachurus-murphyi-s3.jpg` | Maggie Sherriffs | CC BY | [ver original](https://www.inaturalist.org/observations/397978782) |
| *Trachurus murphyi* | `fotos/trachurus-murphyi-1.jpg` | Morita, Kako H. | CC0 | [ver original](https://commons.wikimedia.org/wiki/File:Trachurus_murphyi.jpg) |

## Condiciones para que siga siendo gratis

1. Mantener visibles los créditos de MET Norway, NOAA/PacIOOS, UHSLC y de cada foto.
2. Revisar la planilla de Sernapesca una vez al mes y actualizar la fecha de verificación.
3. Antes de 2029, volver a correr `mareas_chile.py` para extender la tabla de mareas.
4. El aviso (auspiciador) se configura en `app/anuncio.json`.
