import copy
import cPickle
from board import Board

DEF_POS_DICT = "tic_tac.dic"

class Position(object):
    """ simply holds a winner and best move to make 
        things more legible
    """
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


class ABAI(object):
    """ This is a class to use alpha beta pruning """

    def find_move(self,board):
        """ explore all legal moves with minimax
            with alpha beta pruning and return
            a best move
        """
        bmove = None
        if board.next_move > 0:
            alpha = -2
            for move in board.legal_moves():
                board.move(move[0],move[1])
                talpha = self.ab_search(board,alpha,2)
                board.unmove()
                if talpha > alpha:
                    bmove = move
                    alpha = talpha
                    if alpha == 1:
                        return move
        else:
            beta = 2
            for move in board.legal_moves():
                board.move(move[0],move[1])
                tbeta = self.ab_search(board,-2,beta)
                board.unmove()
                if tbeta < beta:
                    bmove = move
                    beta = tbeta
                    if beta == -1:
                        return move
        return bmove

                
    def ab_search(self,board, alpha, beta):
        """ return the value using minimax with alpha beta pruning
            
            board = the board of the current node
            alpha = alpha
            beta  = beta

            search the board with alpha beta pruning and
            return the value of it
       """
        win = board.win_check()
        if not win is None:
            return win
        if board.next_move > 0:
            for move in board.legal_moves():
                board.move(move[0],move[1])
                alpha = max(alpha, self.ab_search(board,alpha,beta))
                board.unmove()
                if beta <= alpha:
                    return alpha
            return alpha
        
        else:
            for move in board.legal_moves():
                board.move(move[0],move[1])
                beta = min(beta, self.ab_search(board,alpha,beta))
                board.unmove()
                if beta <= alpha:
                    return beta
            return beta
