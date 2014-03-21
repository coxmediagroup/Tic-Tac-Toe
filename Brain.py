"""
The Brains of the outfit
"""
from Judge import Judge
from TicTacToeExceptions import TokenPlacementException

class Brain(object):
    """This is our min max guy"""
    def __init__(self, scratch_board, token):
        self.scratch_board = scratch_board
        self.scratch_judge = Judge(self.scratch_board)
        self.opponent = { 'O':'X', 'X':'O' }
        self.token = token
        self.best_move = None


    def evaluateMove(self, p=None, board=None, depth=10):
        """Do the min max evaluation"""
        if board is None:
            board = [' '] * 9
        depth += 1
        scores = []
        moves = []
        #First off are we at the endgame state?
        #if ' ' not in board: #The board is full the game must be done.
        self.scratch_judge.board.tokens = board
        winner, state = self.scratch_judge.evalGame()
        if winner is None and state == 'done':
            return 0
        elif winner == self.token:
            return 10 + depth
        elif winner == self.opponent[self.token]:
            return 10 - depth
        #winner and state are both None

        #Now we build up our moves
        for next_move in self.scratch_judge.board.getPossibleMoves():
            #do the move
            self.scratch_judge.board.addToken(p, next_move)
            #get the new game state

            new_board = self.scratch_judge.board.getBoard()
            #re-evaluate
            score = self.evaluateMove(p=self.opponent[p], board=new_board, depth=depth)
            scores.append(score)
            moves.append(next_move)
            self.scratch_judge.board.tokens[next_move] = ' '

        #now fix the messed up min max that cannot work.
        if p == self.token: #Calc the max.
            max_score = max(scores)
            idx = scores.index(max_score)
            self.best_move = moves[idx]
            return scores[idx]
        else: #Calc the min
            min_score = min(scores)
            idx = scores.index(min_score)
            self.best_move = moves[idx]
            return scores[idx]

