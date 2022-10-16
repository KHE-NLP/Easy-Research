import io
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from cohereGeneration import get_generation, cleanData
from pdfminer.high_level import extract_text

from parsers import get_paragraphs, make_pptx_slides, get_pdf_text


class ContinueServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<form method=\"POST\" action=\"/pdffile\">")
        self.wfile.write(b"<input type=\"file\" name=\"data\" />")
        self.wfile.write(b"<button name=\"submit\">Submit</button>")
        self.wfile.write(b"</form>")

    def do_POST(self):
        line = self.path
        print(line)
        if line[:9] == "/continue":
            content_length = int(self.headers['Content-Length'])
            line = self.rfile.read(content_length)
            line = urllib.parse.parse_qs(line)
            print(line)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            end = list(get_generation([line[b"start"][0].decode()]))
            self.wfile.write(line[b"start"][0] + bytes(end[0].generations[0].text, "utf-8"))
        elif line[:8] == "/pdffile":
            content_length = int(self.headers['Content-Length'])
            line = self.rfile.read(content_length)
            line = urllib.parse.parse_qs(line)
            print(line)
            text = get_paragraphs(extract_text(io.BytesIO(line[b"data"][0])))
            cleanData(text)
            summs = list(get_generation(text, "summary_generator"))
            titles = list(get_generation(summs, "summary_title"))
            ppt = make_pptx_slides([titles[i] + "\n" + summs[i] for i in range(len(titles))])
            self.send_response(200)
            self.send_header("Content-type", "*/*")
            self.end_headers()
            ppt.save(self.wfile)
        elif line[:8] == "/pdflink":
            content_length = int(self.headers['Content-Length'])
            line = self.rfile.read(content_length)
            line = line.split(b"\r\n")[3]
            print(line)
            text = get_paragraphs(get_pdf_text(line.decode()))
            cleanData(text)
            summs = list(get_generation(text, "summary_generator"))
            titles = list(get_generation(summs, "summary_title"))
            ppt = make_pptx_slides([titles[i] + "\n" + summs[i] for i in range(len(titles))])
            self.send_response(200)
            self.send_header("Content-type", "*/*")
            self.end_headers()
            ppt.save(self.wfile)
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"BAD")
        return


if __name__ == "__main__":
    server = HTTPServer(("", 12345), ContinueServer)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
