### Tic Tac Toe server backend written by James Robey, original code from http://snippets.dzone.com/posts/show/ 

### This is the server portion of the tic-tac-toe game, written in python using
### only modules from the standard distribution, for ease of install.

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import urllib

class TicTacToeServer(BaseHTTPRequestHandler):
    """This is a class that functions both an HTTP server and hosts the logic
       needed to win or draw at tic tac toe. It accepts a URL encoded XML string
       on the path and, indeed, the path is the entire input foregoing any query
       strings or other interception of paths as they are not required per spec.
       
       To use this class, initialize it with "TicTacToeServer.serve_forever(PORT_NUMBER)"
       and then pass board states to it to recieve the next board state the computer would
       make.
       
       Please see the strategy.txt document for more information about board state, which
       is used both here and in the front-end (client).
    """
    
    def do_GET(self):
        """machinery to get a request, pass it to the processMove method, and return the result, 
           all via HTTP
        """
        
        #setup the scaffolding for returning XML
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        #extract xml Representation Of Board, process it, and return that xml chunk to the requestor.
        xmlRepresentationOfBoard = urllib.unquote(self.path[1:])
        response = self.processMove(xmlRepresentationOfBoard)
        self.wfile.write(response);

    @staticmethod
    def serve_forever(port):
        """machinery to create an HTTP server on the given port"""
        
        HTTPServer(('', port), TicTacToeServer).serve_forever()
        
    def processMove(self, xmlRepresentationOfBoard):
        """given a representation of the board in XML, return the representation
           that corresponds to the move the computer ("o") would make next.
           This algorithm presumes the human always goes first.
        """
        
        #try to DOM the XML representing the board, If corrupt merely reset the 
        #game, nothing fancier for now.
        try:
            root = ET.XML(xmlRepresentationOfBoard)
        except:
            return """<board></board>"""
            
        #get the board positions and store them. 
        for node in root:
            print node
            
        return xmlRepresentationOfBoard

#kick off a server for use by any number of front ends playing tic tac toe.
if __name__ == "__main__":
    TicTacToeServer.serve_forever(2020)