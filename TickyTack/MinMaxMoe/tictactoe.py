"""
Tools to represent and judge a tic tac toe game.
"""

# global symbols to make the tables look nice:
X, O, _ = "XO_"

kBlank = _
kUnknown = '?'
kTie = '='

class Grid(object):

    def __init__(self, w=3, h=3, initialValue=_):
        self.data = [[initialValue for col in range(w)]
                     for row in range(h)]

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.data)


    def _cell(self, key):
        """
        This is used by __getattr__ and __setattr__, below.
        It allows you to refer to cells as .A1 , .C3 , etc
        """
        try:
            col, row = key
            col = 'ABC'.index(col)
            row = '123'.index(row)
        except ValueError:
            raise ValueError('cell attribute must be in A1:C3, not %s' % key)
        return col, row


    def __setattr__(self, key, value):
        if len(key) == 2:
            col, row = self._cell(key)
            self.data[row][col] = value
        else:
            return super(Grid, self).__setattr__(key, value)

    def __getattr__(self, key):
        if len(key) == 2:
            col, row = self._cell(key)
            return self.data[row][col]
        else:
            return super(Grid, self).__getattribute__(key)



class TicTacToe(Grid):
    """
    Represents the current state of a game.
    """
    def __init__(self, toPlay=X, path='start'):
        super(TicTacToe, self).__init__()
        self.toPlay = toPlay
        self.path = path

    @property
    def moves(self):
        return tuple('%s%s%s' % (self.toPlay, col, row)
                     for col in 'ABC'
                     for row in '123'
                     if getattr(self, '%s%s' % (col, row)) == _)


    def __getattr__(self, key):
        """
        Given an attribute like .XB2, return a new TicTacToe board
        with the move in place.
        """
        if len(key) == 3 and key[0] == self.toPlay:
            t = TicTacToe(toPlay = O if self.toPlay == X else X,
                          path = self.path + '.' + key)
            t.data = [[value for value in row] for row in self.data]
            setattr(t, key[1:], self.toPlay)
            return t
        else:
            return super(TicTacToe, self).__getattr__(key)


    @property
    def isOver(self):
        return len(self.moves) == 0 or self.winner != kUnknown


    # !! no need to be fancy with only a 3x3 grid
    waysToWin = (
        'A1 A2 A3', 'B1 B2 B3', 'C1 C2 C3', # win by column
        'A1 B1 C1', 'A2 B2 C2', 'A3 B3 C3', # win by row
        'A1 B2 C3', 'A3 B2 C1'              # win by diagonal
    )

    @property
    def winner(self):
        for way in self.waysToWin:
            i,j,k = [getattr(self, cell) for cell in way.split()]
            if i==j==k and i != kBlank:
                return i
        return kUnknown if len(self.moves) > 0 else kTie
    


