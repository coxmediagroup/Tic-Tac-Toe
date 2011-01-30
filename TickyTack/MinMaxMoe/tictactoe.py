"""
Tools to represent and judge a tic tac toe game.
"""

# global symbols to make the tables look nice:
X, O, _ = "XO_"

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
            return super(Grid, self).__getattr__(key)



class TicTacToe(Grid):
    """
    Represents the current state of a game.
    """
    def __init__(self):
        super(TicTacToe, self).__init__()
