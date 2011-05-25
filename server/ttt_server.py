### Tic Tac Toe server backend written by James Robey, original code from http://snippets.dzone.com/posts/show/ 

### This is the server portion of the tic-tac-toe game, written in python using
### only modules from the standard distribution, for ease of install.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib, json

from TicTacToe3DField import TicTacToe3DField

class TicTacToeServer(BaseHTTPRequestHandler):
    """This is a class that functions both an HTTP server and hosts the logic
       needed to win or draw at 3D tic tac toe. It accepts a URL encoded JSON string
       via the /turn?game=... path, and any other path returns the document so pointed
       at relative to the current dir (from the server's folder)
       
       In a nutshell it will serve the SWF client and then the client will communicate 
       board state back and forth, playing any number of client instances simultanously.
       
       Please see the strategy.txt document for more information about board state, which
       is used both here and in the front-end (client).
    """
    
    def do_GET(self):
        """machinery to get a request, pass it to the processMove method, and return the result, 
           all via HTTP
        """
        
        #setup the scaffolding for returning XML
        self.send_response(200, 'OK')
        
        #extract the XML representation of the board & process it
        if self.path.startswith("/turn"):
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            queryString = self.path.split("=")[1]
            jsonOfBoard = urllib.unquote(queryString.split('&')[0])
            response = self.processMove(jsonOfBoard)
            self.wfile.write(response);
        else:
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:2020')
            self.end_headers()
            self.wfile.write(file(self.path[1:].split("?")[0]).read())    

    @staticmethod
    def serve_forever(port):
        """machinery to create an HTTP server on the given port"""
        
        HTTPServer(('', port), TicTacToeServer).serve_forever()
        
    def processMove(self, game):
        """given a representation of the board in XML, return the representation
           that corresponds to the move the computer ("o") would make next.
           This algorithm presumes the human always goes first.
        """
        
        #jsonify the input, use it to init the TTT3D field, 
        #determine the next move, and return the board. Tada.
        
        try:
            ttt = TicTacToe3DField(json.loads(game))
        except:
            ttt = TicTacToe3DField()
            
        response = "<data>%s</data>"%json.dumps(ttt.determineMove())
        print response
        return response

#kick off a server for use by any number of front ends playing tic tac toe.
if __name__ == "__main__":
    TicTacToeServer.serve_forever(22222)
    
