"""
Never loose algo from:
http://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
"""
import copy
from collections import OrderedDict


POS = {0: (0, 0), 1: (0, 1), 2: (0, 2),
       3: (1, 0), 4: (1, 1), 5: (1, 2),
       6: (2, 0), 7: (2, 1), 8: (2, 2)} 
class DisplayTicTacToe:
    def __init__(self, ttt):
        self.ttt = ttt

    def output(self, board=None):
        """
        Print the board.
        """
        if board is None:
            board = self.ttt.board
        for i in range(3):
            print board[i]
        print


    def as_dict(self):
        """
        Returns a dict, suitable for passing to render()
        """
        dct = {}
        for idx, xy in POS.items():
            x, y = xy   
            dct[idx+1] = self.ttt.board[x][y]

        return dct
 

class TicTacToe:
    def __init__(self, xo='X', first=False):
        self.board = [[None]*3, [None]*3, [None]*3]
        self.xo = xo
        if first:
            self.ai_move()

    def make_move(self, idx):
        """
        Move the opponent on the board.
        """
        if self.xo == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        x, y = POS[idx-1]
        self.board[x][y] = opponent

    def won(self):
        """
        The game has been won by somebody.
        """
        MARKS = ['X', 'O']

        # X
        for i in range(3):
            for mark in MARKS:
                if self.places_match(None, [(i, 0, mark), (i, 1, mark), 
                                            (i, 2, mark)]):
                    return mark
        # Y
        for i in range(3):
            for mark in MARKS:
                if self.places_match(None, [(0, i, mark), (1, i, mark), 
                                            (2, i, mark)]):
                    return mark
        
        #diagonals
        for mark in MARKS:
            if self.places_match(None, [(0, 0, mark), (1, 1, mark), 
                                        (2, 2, mark)]):
                return mark

        for mark in MARKS:
            if self.places_match(None, [(0, 2, mark), (1, 1, mark), 
                                        (2, 0, mark)]):
                return mark
            
        # Cats game
        for i in range(9):
            x, y = POS[i]
            if self.board[x][y] is None:
                return None
    
        return 'cats'
        
        
        

    def has_win_move(self, board=None, mark='O'):
        """
        mark has a move where they can win

        Returns a where to place the opposite mark to bloack the win.
        """
        if board is None:
            board = self.board

        winning_moves = []


        # First along the x axis
        for i in range(3):
            if self.places_match(board, [(i, 0, mark), (i, 1, mark),
                                         (i, 2, None)]):
                winning_moves.append((i, 2))
            if self.places_match(board, [(i, 0, mark), (i, 2, mark),
                                         (i, 1, None)]):
                winning_moves.append((i, 1))
            if self.places_match(board, [(i, 1, mark), (i, 2, mark),
                                         (i, 0, None)]):
                winning_moves.append((i, 0))

        # Then along the y axis
        for i in range(3):
            if self.places_match(board, [(0, i, mark), (1, i, mark),
                                         (2, i, None)]):
                winning_moves.append((2, i))
            if self.places_match(board, [(0, i, mark), (2, i, mark),
                                         (1, i, None)]):
                winning_moves.append((1, i))
            if self.places_match(board, [(1, i, mark), (2, i, mark),
                                         (0, i, None)]):
                winning_moves.append((0, i))

        # Now diagonal
        # (1,1) is always going to be set for diagonals, all we need to do is
        # match the corners.
        diagonals = {(0, 0): (2, 2),
                     (2, 2): (0, 0),
                     (0, 2): (2, 0),
                     (2, 0): (0, 2)}

        for diags, ret in diagonals.items():
            if (self.places_match(board, [(diags[0], diags[1], mark),
                                         (1, 1, mark), (ret[0], ret[1], None)])):
                winning_moves.append(ret)

        winning_moves = list(set(winning_moves))

        if len(winning_moves) == 1:
            return winning_moves[0]
        elif winning_moves:
            return winning_moves
        else:
            return False
            


    def has_fork(self, mark='O'):
        """
        A fork is when there exists two possibilities that create a winning
        move. 
        """

        for i in range(9):
            board = copy.deepcopy(self.board)
            x, y = POS[i]
    
            if board[x][y] is not None: 
                continue

            board[x][y] = mark
            wins = self.has_win_move(board)
            if type(wins) is type([]) and len(wins) == 2:
                return POS[i]

    def places_match(self, board=None, places=None):
        """
        Check if the places are taken by xo.

        places is a list of tuple of (x,y,xo).
        """
        if board is None:
            board = self.board

        found=True
        if not places:
            return False

        for place in places:
            x, y, xo = place
            if board[x][y] != xo:
                found = False

        return found
    
    def ai_move(self):
        if self.xo == 'X':
            opponent = 'O'
        else:
            opponent = 'X'

        # win move for me
        where = self.has_win_move(mark=self.xo)
        if where:
            self.board[where[0]][where[1]] = self.xo
            return 

        # win move for opponent
        where = self.has_win_move(mark=opponent)
        if where:
            self.board[where[0]][where[1]] = self.xo
            return 

        #Block an opponent's fork
        #Special Case
        if self.board[0][0] == opponent and self.board[2][2] == opponent:
            self.board[0][1] = self.xo
            return 

        where = self.has_fork(mark=opponent)
        if where:
            self.board[where[0]][where[1]] = self.xo
            return 

        #Look for our own forks
        where = self.has_fork()
        if where:
            self.board[where[0]][where[1]] = self.xo
            return 
       
        #Center 
        if self.board[1][1] is None:
            self.board[1][1] = self.xo
            return 

        # Opposite Corner
        CORNERS = {(0, 0): (2, 2), (0, 2): (2, 0),
                   (2, 0): (0, 2), (2, 2): (0, 0)}
        CORNERS = OrderedDict(sorted(CORNERS.items(), key=lambda t: t[0]))
        for corner, opposite in CORNERS.items():
            x, y = corner
            if self.board[x][y] == opponent:
                x, y = opposite
                if self.board[x][y] is None:
                    self.board[x][y] = self.xo
                    return 

        # Empty corner
        for corner in CORNERS.keys():
            x, y = corner
            if self.board[x][y] is None:
                self.board[x][y] = self.xo
                return 

        # Empty side
        SIDES = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for side in SIDES:
            x,y = side
            if self.board[x][y] is None:
                self.board[x][y] = self.xo
                return 
    
