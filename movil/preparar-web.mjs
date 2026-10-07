// Copia la app web ya armada (../app, después de construir.py) a www/, que es lo que va dentro del APK.
// Deja fuera lo que solo sirve en el navegador o en el computador.
import { cpSync, rmSync, existsSync } from "node:fs";
import { join, relative, sep } from "node:path";

const origen = join(import.meta.dirname, "..", "app");
const destino = join(import.meta.dirname, "www");
const fuera = new Set(["src", "publicar.html", "sw.js", "version.json"]);

if (!existsSync(join(origen, "archivos.json"))) throw new Error("Falta app/archivos.json: corre antes python app/src/construir.py");
rmSync(destino, { recursive: true, force: true });
cpSync(origen, destino, { recursive: true, filter: (p) => !fuera.has(relative(origen, p).split(sep)[0]) });
console.log("www listo desde", origen);
