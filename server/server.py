from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from os.path import basename
from os import chdir
import time

class DynamicContentRequestHandler(SimpleHTTPRequestHandler):
    def _send_head(self, content, mimeType):
        self.send_response(200)
        self.send_header("Content-type", mimeType)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()

    def _getDynamicContent(self):
        parsed = urlparse(self.path)
        path = parsed.path
        methodName = basename(path)
        if hasattr(self, methodName):
            method = getattr(self, methodName)
            queryParms = parse_qs(parsed.query)
            return method(path, queryParms)
        else:
            return None

    def do_GET(self):
        dynamicContent = self._getDynamicContent()
        if dynamicContent is None:
            super().do_GET()
        else:
            content, mimeType = dynamicContent
            self._send_head(content, mimeType)
            self.wfile.write(bytes(content, "utf-8"))

    def do_HEAD(self):
        content = self._getDynamicContent()
        if content is None:
            super().do_HEAD()
        else:
            content, mimeType = content
            self._send_head(content, mimeType)

def run(hostName, hostPort, requestHandler):
    chdir('static')     
    myServer = HTTPServer((hostName, hostPort), requestHandler)
    print("[%s] Server started on %s:%s" % (time.asctime(), hostName, hostPort))
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received.  Shutting down server...")
    finally:
        myServer.server_close()
        print("[%s] Server stopped on %s:%s" % (time.asctime(), hostName, hostPort))
