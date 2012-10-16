from itertools import izip, izip_longest, chain 

all_trips_dct = {1: (0, 3, 6),
                 2: (2,),
                 3: (0, 1, 2),
                 4: (0,)
                }
all_trips = set()

def three_cons(st, inc):
    "Returns sequence of '3 in a row', starting with st and incremented by inc"
    return st, st + inc, st + inc * 2

for inc, starts in all_trips_dct.iteritems():
    for start in starts:
        all_trips.add(three_cons(start, inc))

x, o = 'x', 'o'

class Board(object):
    """Tic tac toe board. Positions on board are given by index inlist of
    length 9.
    """
    def __init__(self):
        "Start off with empty board--empty sets of x's and o's"
        self.xs = set()
        self.os = set()
        self.grid = [' '] * 9
        row_str = '%s|%s|%s\n'
        sep_str = '-' * 5 + '\n'
        self.board_str = sep_str.join([row_str] * 3)
        self.range = set([0, 1, 2])
        self._empty = None

    def __repr__(self):
        return self.board_str % tuple(self.grid)

    def __getitem__(self, idx):
        return self.grid[idx]

    def __setitem__(self, idx, val):
        self._empty = None
        self.grid[idx] = val

    def l2g(self, coord):
        """Convert list coordinates (0-8) to grid coordinates (0-2, 0-2).
        Grid coords are in (row, col) format.
        """
        return coord / 3, coord % 3

    def g2l(self, i, j=None):
        """Convert grid coordinates (0-2, 0-2) to list coordinates (0-8).
        Can pass grid coords individually or as tuple."""        
        if j is None:
            i, j = i
        return i * 3 + j

    def any2g(self, *coord):
        "Returns coordinates in grid format regardless of input format"
        if len(coord) == 2:
            return coord
        return self.l2g(*coord)

    def any2l(self, *coord):
        "Returns coordinates in index format regardless of input format"
        if len(coord) == 1:
            return coord[0]
        return self.g2l(*coord)

    @property
    def empty_cells(self):
        "Returns set of empty cells on board"
        if self._empty is None:
            self._empty = set([i for i, s in enumerate(self.grid) if s == ' '])
        return self._empty

    def isempty(self, coord):
        coord = self.any2l(coord)
        return coord in self.empty_cells

    def adj(self, coord, include_diag=False, only_empty=False):
        i, j = self.any2g(coord)
        other_rows = [r for r in (i + 1, i - 1) if r in self.range]
        other_cols = [c for c in (j + 1, j - 1) if c in self.range]
        vert = izip_longest(other_rows, [j], fillvalue=j)
        horz = izip_longest([i], other_cols, fillvalue=i)
        vert, horz = list(vert), list(horz)
        lr, lc = map(len, (other_rows, other_cols))
        if lr < lc:
            other_rows *= lc
        elif lr > lc:
            other_cols *= lr
        diag = izip(other_rows, other_cols)
        ret_args = [vert, horz] + ([diag] if include_diag else [])
        return chain(*ret_args)