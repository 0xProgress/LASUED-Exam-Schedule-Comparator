import http.server
import urllib.request
import urllib.parse
import ssl
import os

API_BASE = "https://docket.support.lasued.edu.ng/api"


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        target_url = API_BASE + self.path
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            target_url,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        try:
            with urllib.request.urlopen(req, context=ctx) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(e.read())

    def log_message(self, format, *args):
        print(f"[Proxy] {args[0]}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    print(f"Proxy running on port {port}")
    http.server.HTTPServer(("0.0.0.0", port), ProxyHandler).serve_forever()