import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from cohereGeneration import get_generation


class ContinueServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<form method=\"POST\" action=\"/continue\">")
        self.wfile.write(b"<input name=\"start\" />")
        self.wfile.write(b"</form>")

    def do_POST(self):
        line = self.path
        print(line)
        if line[:9] != "/continue":
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"BAD")
            return
        content_length = int(self.headers['Content-Length'])
        line = self.rfile.read(content_length)
        line = line.split(b"=")[1]
        line = line.replace(b"+", b" ")
        print(line)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        end = list(get_generation([line.decode("ascii")]))
        self.wfile.write(line + bytes(end[0].generations[0].text, "utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("", 12345), ContinueServer)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
