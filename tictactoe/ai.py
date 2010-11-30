import copy
import cPickle
from board import Board

DEF_POS_DICT = "tic_tac.dic"

class Position(object):
    def __init__(self,winner,move):
        self.winner = winner
        self.move = copy.copy(move)

class AI(object):
    def __init__(self):
        """ attempts to load the move dict
            if it fails it build a new one """
        self.board = Board()
        self.moves = {}
        try:
            self.moves = cPickle.load(open(DEF_POS_DICT,'rb'))
        except IOError:
            self.build_moves()

    def build_moves(self):
        """ explore all positions below self.board 
            save them in the moves dictionary """
        board = self.board
        player = board.next_move
        #is the game over
        win = board.win_check()
        if win:
            return win
        open_moves = board.legal_moves()
        if not open_moves:
            return 0
        #have we seen this position before
        moves = self.moves
        try:
            return moves[board.key()].winner
        except KeyError:
            pass            
        best = -2
        best_move = None
        for mv in open_moves:
            board.move(mv[0],mv[1])
            win = self.build_moves()
            val = win * player
            board.unmove()
            if val > best:
                best = val
                best_move = mv
        best *= player
        moves[board.key()] = Position(best,best_move)
        return best

    def find_move(self, board):
        """ find a move in the dictionary if it's not 
            there explore more and return it.
            since build_moves doesn't do any pruning 
            it should always be there """
        try:
            return self.moves[board.key()].move
        except KeyError:
            pass
        self.board.board = copy.deepcopy(board.board)
        self.build_moves()
        return self.moves[board.key()].move

    def sav(self):
        f = open(DEF_POS_DICT,'wb')
        cPickle.dump(self.moves,f,2)
        f.close()
