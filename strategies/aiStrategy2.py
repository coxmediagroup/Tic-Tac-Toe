'''
This strategy file should just define a bestMove() function for the TicTacToe class.

Since the function is a member of TicTacToe, it has access to all of that class's
attributes: i.e. numTurn, whosTurn, aiMark, evalForkability(), evalDanger(),
availSquares, etc.

The bestMove() function *MUST* return an int representing a square to move to
no matter what!
'''

# Example dumb strategy
def bestMove(self):
    return sorted(self.availSquares)[0]
