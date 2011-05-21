### Tic Tac Toe server backend written by James Robey, original code from http://snippets.dzone.com/posts/show/654

### This is the server portion of the tic-tac-toe game, written in python using
### only modules from the standard distribution, for ease of install.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("hello")

    @staticmethod
    def serve_forever(port):
        HTTPServer(('', port), MyServer).serve_forever()

if __name__ == "__main__":
    MyServer.serve_forever(9090)