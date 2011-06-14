from TicTacToeExceptions import TokenPlacementException

class Board(object):


    def __init__(self):
        self.tokens = [None] * 9

    def addToken(self, token, idx):
        if not self.tokens[idx]:
            self.tokens[idx] = token
        else:
            msg = "Token at %s" % idx
            raise TokenPlacementException(msg)

         


    def getBoard(self):
        return self.tokens

