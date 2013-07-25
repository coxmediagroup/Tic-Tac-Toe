"""
The Tic Tac Toe Board

"""
from itertools import chain
from pprint import pformat

board_template ="""
  0   1   2
0 {0[0]} | {0[1]} | {0[2]}
 -----------
1 {1[0]} | {1[1]} | {1[2]}
-----------
2 {2[0]} | {2[1]} | {2[2]}
"""

X='X'
O='O'
STALEMATE='STALEMATE'

_input_map = {
            1:(0,0), 2:(0,1), 3:(0,2),
            4:(1,0), 5:(1,1), 6:(1,2),
            7:(2,0), 8:(2,1), 9:(2,2),
        }

class Board(object):
    """docstring for ClassName"""



    def __init__(self):
        self._spaces = [[1,2,3],
                        [4,5,6],
                        [7,8,9]]

    def __repr__(self):
        return pformat(self._spaces)

    def __str__(self):
        return board_template.format(*self._spaces)

    def __getitem__(self, key):
        try:
            r,c = _input_map[key]
        except KeyError, e:
            raise IndexError("Invalid Cell Key")
        return self._spaces[r][c]

    def __setitem__(self, key, player):
        assert player in (X,O)
        try:
            r,c = _input_map[key]
        except KeyError, e:
            raise IndexError("Invalid Cell Key")
        self._spaces[r][c]
        assert self._spaces[r][c] not in (X,O)
        self._spaces[r][c] = player

    def cells(self):
        return (c for r in self._spaces for c in r )

    def rows(self): #"yield from" is not available until 3.3
        return (tuple(row) for row in self._spaces)

    def cols(self):#"yield from" is not available until 3.3
        return (tuple(row) for row in zip(*self._spaces))

    def diags(self):
        yield (self._spaces[0][0], self._spaces[1][1], self._spaces[2][2])
        yield (self._spaces[2][0], self._spaces[1][1], self._spaces[0][2])

    def rows_cols_diags(self): #"yield from" is not available until 3.3
        return chain(self.rows(), self.cols(), self.diags())

    def check_win(self):
        for rcd in self.rows_cols_diags():
            if (rcd[0] == rcd[1] == rcd[2]) and rcd[0] in (X,O):
                return rcd[0]
        for space in self.cells():
            if space not in (X,O):
                break
        else:
            return STALEMATE
        return None








