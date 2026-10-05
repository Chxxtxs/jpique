# jPique

App gratuita para pesca recreativa en la zona central de Chile: mareas, vedas, tallas, cuotas, actividad de peces, luna, bitácora de capturas con carpetas y licencia de pesca. Se instala en el celular desde el navegador y funciona sin señal.

## Cómo se actualiza

1. Haces un cambio (en `app/src/index.template.html`, `app/anuncio.json`, las fotos, etc.).
2. Lo subes a GitHub (`git add .`, `git commit -m "qué cambiaste"`, `git push`).
3. GitHub publica la app sola en unos 2 minutos (pestaña **Actions**).
4. Quien tenga la app abierta ve el aviso **«Hay una versión nueva de la app → Actualizar»**. También pueden ir a **Normas → Versión de la app → Buscar actualización**. Sus capturas, carpetas y licencia no se borran.

Además, todos los días a las 06:15 GitHub vuelve a armar la app con el pronóstico del día, para que funcione sin señal con datos frescos. Eso no muestra el aviso de versión nueva.

> GitHub pausa las tareas diarias si el repositorio pasa 60 días sin cambios. Para reactivarlas: pestaña **Actions → Publicar app → Enable workflow**.

## Cambiar la tienda recomendada

Edita `app/anuncio.json`. Con `"activo": false` el aviso desaparece. El logo va en `app/` con un nombre que empiece con `anuncio-`.

## Probar en el computador

```
python app/src/construir.py --offline
python app/src/servidor.py 5179
```

Luego abre http://localhost:5179 (o, desde el celular en la misma red Wi-Fi, la dirección que imprime el servidor).

## Mantenimiento

| Qué | Cuándo | Cómo |
|---|---|---|
| Vedas, tallas y cuotas | Una vez al mes | Revisar la planilla de Sernapesca y editar `ESPECIES` en `app/src/index.template.html` |
| Tabla de mareas | Antes de 2030 | `pip install utide numpy` y `python app/src/mareas_valparaiso.py` |
| Registro de fuentes | Si cambian las fotos | `python app/src/registro_fuentes.py` |

## Costo

$0. Todas las fuentes permiten uso comercial gratis (también con publicidad). Detalle en [FUENTES_Y_LICENCIAS.md](FUENTES_Y_LICENCIAS.md).
