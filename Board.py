from TicTacToeExceptions import TokenPlacementException

class Board(object):


    def __init__(self):
        self.tokens = [None] * 9

    def addToken(self, token, idx):
        """Add a token to the board or raise an exception

        str token  "x" or "o"
        int idx    0-8"""

        if  idx > 8 or idx < 0:
            msg = "Invalid index %s " % idx
            raise TokenPlacementException(msg)

        if not self.tokens[idx]:
            self.tokens[idx] = token
        else:
            msg = "Token at %s" % idx
            raise TokenPlacementException(msg)

         


    def getBoard(self):
        return self.tokens

