from Board import Board
from Judge import Judge
from TicTacToeExceptions import TokenPlacementException

class Brain(object):

    token = 'x'
    def __init__(self):
        self.scratch_board = Board()
        self.scratch_judge = Judge(self.scratch_board)
        self.opponent = { 'o':'x', 'x':'o' }


    def evaluateMove(self, move, p=token, board=None):
        try:
            if not board:
                board = [None] * 9
            self.scratch_board.tokens = board 
            self.scratch_board.addToken(p, move)
            new_board = self.scratch_board.getBoard()
            outcome = self.scratch_judge.evalGame()
            if outcome is not None and 'done' in outcome:
                return self.decide(self.scratch_judge.isWinner())

            outcomes = (
                    self.evaluateMove(next_move, p=self.opponent[p], board=new_board) 
                    for next_move in self.scratch_board.getPossibleMoves())
            if p == 'o':
                min_outcome = 1
                return min(outcomes) #searching whole list takes a while
                for o in outcomes:
                    if o == -1:
                        return o 
                    min_outcome = min(o,min_outcome)
                return min_outcome
            else:
                return max(outcomes)
                max_outcome = 1
                for o in outcomes:
                    if o == 1:
                        return o 
                    max_outcome = min(o,max_outcome)
                return max_outcome

        finally:
            self.scratch_board.undo(move)
        
    def decide(self, winner):
        """Decide if it is a good thing our a bad thing"""
        if winner == self.token:
            return 1
        if winner == None:
            return 0
        return -1
