#Tic-Tac-Toe#

Unbeatable tic-tac-toe AI. Implemented using Python, bottle.py, mongodb, and AngularJS.

##Dependencies##

MongoDB and pymongo are required to run this. If your mongodb installation is different from the default (on Ubuntu, at least), you'll need to edit the configuration settings in movecache.py to reflect this.

##To run##

Simply run `python server.py` and point your browser at <http://localhost:8000>.

##High-Level Overview##

The client stores all the game state and simply sends this state to the server to get what the computer's move would be for a given game state. This is accomplished in static/TicTacToeCtrl.js .

When a request is received (handled in server.py), the state information is used to build a board object (defined in board.py). This is then passed to a MinimaxCalculator object (defined in minimax.py), which uses this object to run the Minimax algorithm to determine the best move.

In order to minimize the depth of the recursion from the Minimax algorithm, the result of each call is cached in mongodb. A MoveCache (defined in movecache.py) object is used to help simplify the interface to mongodb by making the interface work like a dictionary.


