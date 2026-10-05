"""Lugares de pesca de jPique: de Arica a Magallanes.

Cada lugar: (id, nombre, región, tipo, latitud, longitud).
Tipos: orilla (playa), roquerío, río, lago, embalse. Las coordenadas son aproximadas (±2 km).
construir.py asigna a cada lugar de mar su mareógrafo y su celda de oleaje más cercanos.
"""

# De norte a sur (así se ordena el selector de la app)
REGIONES = ["Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo", "Valparaíso", "Metropolitana",
            "O'Higgins", "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"]

LUGARES = [
    # Arica y Parinacota
    ("arica-chinchorro", "Arica · Playa Chinchorro", "Arica y Parinacota", "orilla", -18.435, -70.298),
    ("arica-lisera", "Arica · La Lisera y el Morro", "Arica y Parinacota", "roquerío", -18.490, -70.325),
    # Tarapacá
    ("iquique-cavancha", "Iquique · Playa Cavancha", "Tarapacá", "orilla", -20.236, -70.140),
    ("iquique-chanavayita", "Iquique · Caleta Chanavayita", "Tarapacá", "roquerío", -20.715, -70.185),
    # Antofagasta
    ("antofagasta-balneario", "Antofagasta · Balneario Municipal", "Antofagasta", "orilla", -23.650, -70.405),
    ("antofagasta-portada", "Antofagasta · La Portada", "Antofagasta", "roquerío", -23.526, -70.503),
    ("mejillones", "Mejillones · Playa", "Antofagasta", "orilla", -23.100, -70.450),
    ("tocopilla", "Tocopilla · Caleta", "Antofagasta", "roquerío", -22.090, -70.205),
    ("taltal", "Taltal · Caleta", "Antofagasta", "roquerío", -25.405, -70.485),
    # Atacama
    ("bahia-inglesa", "Caldera · Bahía Inglesa", "Atacama", "orilla", -27.115, -70.855),
    ("chanaral", "Chañaral · Playa", "Atacama", "orilla", -26.345, -70.640),
    ("huasco", "Huasco · Caleta", "Atacama", "roquerío", -28.460, -71.225),
    # Coquimbo
    ("laserena-faro", "La Serena · Faro y playas", "Coquimbo", "orilla", -29.907, -71.280),
    ("coquimbo-herradura", "Coquimbo · La Herradura", "Coquimbo", "orilla", -29.970, -71.355),
    ("tongoy", "Tongoy · Playa Grande", "Coquimbo", "orilla", -30.255, -71.495),
    ("losvilos", "Los Vilos · Caleta", "Coquimbo", "roquerío", -31.915, -71.515),
    ("pichidangui", "Pichidangui", "Coquimbo", "orilla", -32.135, -71.535),
    # Valparaíso (zona central)
    ("zapallar", "Zapallar", "Valparaíso", "roquerío", -32.550, -71.460),
    ("papudo", "Papudo", "Valparaíso", "orilla", -32.507, -71.455),
    ("quintero", "Quintero · Loncura", "Valparaíso", "orilla", -32.775, -71.535),
    ("concon", "Concón · Roca Oceánica", "Valparaíso", "roquerío", -32.900, -71.505),
    ("renaca", "Viña del Mar · Reñaca", "Valparaíso", "roquerío", -32.975, -71.545),
    ("valparaiso", "Valparaíso · Caleta Portales", "Valparaíso", "roquerío", -33.030, -71.600),
    ("algarrobo", "Algarrobo", "Valparaíso", "orilla", -33.360, -71.690),
    ("cartagena", "Cartagena", "Valparaíso", "orilla", -33.550, -71.620),
    ("sanantonio", "San Antonio · Molo", "Valparaíso", "orilla", -33.590, -71.620),
    ("llolleo", "Llolleo · Desembocadura Maipo", "Valparaíso", "orilla", -33.625, -71.635),
    ("juanfernandez", "Isla Juan Fernández · San Juan Bautista", "Valparaíso", "roquerío", -33.640, -78.835),
    ("hangaroa", "Isla de Pascua · Hanga Roa", "Valparaíso", "roquerío", -27.150, -109.430),
    # Metropolitana
    ("maipo", "Río Maipo · San José", "Metropolitana", "río", -33.640, -70.350),
    ("aculeo", "Laguna de Aculeo", "Metropolitana", "lago", -33.830, -70.910),
    ("elyeso", "Embalse El Yeso", "Metropolitana", "embalse", -33.667, -70.083),
    # O'Higgins
    ("navidad", "Matanzas · Navidad", "O'Higgins", "orilla", -33.960, -71.890),
    ("pichilemu", "Pichilemu · Punta de Lobos", "O'Higgins", "roquerío", -34.425, -72.050),
    ("bucalemu", "Bucalemu", "O'Higgins", "orilla", -34.640, -72.060),
    ("rapel", "Embalse Rapel", "O'Higgins", "embalse", -34.100, -71.500),
    ("cachapoal", "Río Cachapoal · Coya", "O'Higgins", "río", -34.200, -70.550),
    # Maule
    ("constitucion", "Constitución · Piedra de la Iglesia", "Maule", "roquerío", -35.330, -72.430),
    ("pelluhue", "Pelluhue · Curanipe", "Maule", "orilla", -35.840, -72.630),
    ("colbun", "Embalse Colbún", "Maule", "embalse", -35.680, -71.300),
    ("vichuquen", "Lago Vichuquén", "Maule", "lago", -34.820, -72.050),
    # Ñuble
    ("cobquecura", "Cobquecura", "Ñuble", "orilla", -36.135, -72.790),
    ("itata", "Río Itata · Coelemu", "Ñuble", "río", -36.490, -72.700),
    # Biobío
    ("dichato", "Dichato", "Biobío", "orilla", -36.550, -72.930),
    ("tumbes", "Talcahuano · Caleta Tumbes", "Biobío", "roquerío", -36.630, -73.095),
    ("coronel", "Coronel · Playa Blanca", "Biobío", "orilla", -37.030, -73.150),
    ("lebu", "Lebu", "Biobío", "orilla", -37.605, -73.655),
    ("biobio", "Río Biobío · Santa Bárbara", "Biobío", "río", -37.670, -72.020),
    ("lanalhue", "Lago Lanalhue", "Biobío", "lago", -37.915, -73.300),
    ("laja", "Lago Laja", "Biobío", "lago", -37.350, -71.350),
    # La Araucanía
    ("saavedra", "Puerto Saavedra", "La Araucanía", "orilla", -38.785, -73.400),
    ("villarrica", "Lago Villarrica · Pucón", "La Araucanía", "lago", -39.280, -71.950),
    ("trancura", "Río Trancura · Pucón", "La Araucanía", "río", -39.270, -71.850),
    ("calafquen", "Lago Calafquén · Lican Ray", "La Araucanía", "lago", -39.485, -72.145),
    ("tolten", "Río Toltén · Villarrica", "La Araucanía", "río", -39.280, -72.220),
    # Los Ríos
    ("niebla", "Niebla · Corral", "Los Ríos", "orilla", -39.865, -73.400),
    ("mehuin", "Mehuín", "Los Ríos", "orilla", -39.430, -73.210),
    ("callecalle", "Río Calle-Calle · Valdivia", "Los Ríos", "río", -39.815, -73.230),
    ("panguipulli", "Lago Panguipulli", "Los Ríos", "lago", -39.640, -72.330),
    ("rinihue", "Lago Riñihue", "Los Ríos", "lago", -39.780, -72.350),
    ("ranco", "Lago Ranco", "Los Ríos", "lago", -40.220, -72.400),
    # Los Lagos
    ("ancud", "Ancud · Chiloé", "Los Lagos", "orilla", -41.870, -73.830),
    ("castro", "Castro · Chiloé", "Los Lagos", "orilla", -42.470, -73.770),
    ("pelluco", "Puerto Montt · Pelluco", "Los Lagos", "orilla", -41.470, -72.910),
    ("calbuco", "Calbuco", "Los Lagos", "orilla", -41.770, -73.130),
    ("chaiten", "Chaitén", "Los Lagos", "orilla", -42.920, -72.710),
    ("llanquihue", "Lago Llanquihue · Puerto Varas", "Los Lagos", "lago", -41.320, -72.985),
    ("rupanco", "Lago Rupanco", "Los Lagos", "lago", -40.820, -72.550),
    ("puyehue", "Lago Puyehue", "Los Lagos", "lago", -40.670, -72.450),
    ("petrohue", "Río Petrohué", "Los Lagos", "río", -41.140, -72.400),
    ("futaleufu", "Río Futaleufú", "Los Lagos", "río", -43.185, -71.865),
    # Aysén
    ("chacabuco", "Puerto Chacabuco", "Aysén", "orilla", -45.465, -72.820),
    ("cisnes", "Puerto Cisnes", "Aysén", "orilla", -44.730, -72.680),
    ("simpson", "Río Simpson · Coyhaique", "Aysén", "río", -45.550, -72.030),
    ("gcarrera", "Lago General Carrera · Chile Chico", "Aysén", "lago", -46.540, -71.720),
    ("baker", "Río Baker · Cochrane", "Aysén", "río", -47.250, -72.570),
    # Magallanes
    ("puntaarenas", "Punta Arenas · Costanera", "Magallanes", "orilla", -53.155, -70.905),
    ("natales", "Puerto Natales", "Magallanes", "orilla", -51.730, -72.500),
    ("williams", "Puerto Williams · Canal Beagle", "Magallanes", "orilla", -54.935, -67.620),
    ("parrillar", "Laguna Parrillar", "Magallanes", "lago", -53.400, -71.350),
    ("fagnano", "Lago Fagnano", "Magallanes", "lago", -54.550, -67.800),
]

# Huso horario de cada región (Aysén y Magallanes usan hora fija UTC-3 todo el año)
TZ_REGION = {"Aysén": "America/Punta_Arenas", "Magallanes": "America/Punta_Arenas"}
TZ_LUGAR = {"hangaroa": "Pacific/Easter"}
