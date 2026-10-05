"""Sirve la app para probarla en el computador o en el celular (misma red Wi-Fi).

Uso:  python servidor.py
Luego abre http://localhost:5178 en el computador, o la dirección que se imprime en el celular.
"""
import http.server, os, socket, socketserver, sys

PUERTO = int(sys.argv[1]) if len(sys.argv) > 1 else 5178
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class Manejador(http.server.SimpleHTTPRequestHandler):
    # Windows a veces entrega .js como text/plain, y el navegador rechaza así el modo sin conexión
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".js": "text/javascript", ".webmanifest": "application/manifest+json", ".json": "application/json"}

    def __init__(self, *a, **k):
        super().__init__(*a, directory=CARPETA, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); return ip
    except OSError:
        return "IP-DE-ESTE-PC"


if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", PUERTO), Manejador) as srv:
        print(f"Computador: http://localhost:{PUERTO}")
        print(f"Celular (misma red Wi-Fi): http://{ip_local()}:{PUERTO}")
        srv.serve_forever()
