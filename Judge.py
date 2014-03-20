"""
This is the rules object for the game.

"""


class Judge(object):

    def __init__(self, board):
        self.board = board

    def evalGame(self):
        """Evaluate where we are in the game"""

        result = self.isWinner()
        if result:
            return [result, "done"]
        if ' ' not in self.board.tokens:
            return [result, "done"]
        return [None, None]

    def isWinner(self):
        """Determine winner in current state

        return "x", "o", or None

        """

        winners = [[0,1,2],[3,4,5],[6,7,8], # vertical
                   [0,3,6],[1,4,7],[2,5,8], # horizontal
                   [0,4,8],[2,4,6]]         # diagonal
        winner = None
        for row in winners:
            rows = [self.board.tokens[i] for i in row]
            match = self.rowsEqual(rows)
            if  self.board.tokens[row[0]] != ' ' and match:
                return self.board.tokens[row[0]]

        return winner




    def rowsEqual(self, rows):
        """returns True if all the elements in a list are equal, or if the list is empty."""

        result = not rows or rows == [rows[0]] * len(rows)
        return result
