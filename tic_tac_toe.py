from itertools import izip, izip_longest, chain, ifilter, combinations, cycle
import random

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
    def __init__(self, autosym=x, playersym=o):
        "Start off with empty board--empty sets of x's and o's"
        self.auto = autosym
        self.player = playersym
        self.grid = [' '] * 9
        row_str = '%s|%s|%s\n'
        sep_str = '-' * 5 + '\n'
        self.board_str = sep_str.join([row_str] * 3)[:-1]
        self.range = set([0, 1, 2])
        self._empty = None
        self._corners = (0, 2, 6, 8)
        self._edges = (1, 3, 5, 7)

    def __repr__(self):
        return self.board_str % tuple(self.grid)

    def __getitem__(self, idx):
        return self.grid[idx]

    def __setitem__(self, idx, val):
        self._empty = None
        self.grid[idx] = val

    def clear(self, idx):
        self[idx] = ' '

    def clearall(self):
        for i in range(len(self.grid)):
            self.clear(i)

    def setboard(self, it=range(9)):
        "Starting from the 0th cell, fill in board with values from it."
        for i, val in enumerate(it):
            try:
                self[i] = val
            except IndexError, e:
                return

    def clone(self):
        b2 = type(self)(autosym=self.auto, playersym=self.player)
        b2.grid = self.grid[:]
        return b2

    def findall(self, val):
        "Yields indices of grid having value `val`."
        for idx, val2 in enumerate(self.grid):
            if val == val2:
                yield idx

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

    def isempty(self, *coord):
        coord = self.any2l(*coord)
        return coord in self.empty_cells

    def iscorner(self, *coord):
        coord = self.any2l(*coord)
        return coord in self._corners

    def isedge(self, *coord):
        coord = self.any2l(*coord)
        return coord in self._edges

    def emptycorners(self):
        return [i for i in self.empty_cells if self.iscorner(i)]

    def emptyedges(self):
        return [i for i in self.empty_cells if self.isedge(i)]

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
        if only_empty:
            return ifilter(lambda x: self.isempty(*x), chain(*ret_args))
        return chain(*ret_args)

    def won(self, sym=x):
        for triplet in combinations(self.findall(sym), 3):
            if triplet in all_trips:
                return True
        return False

    def winnable(self, sym=x):
        for cell in self.empty_cells:
            test = self.clone()
            test[cell] = sym
            if test.won(sym):
                return cell
        return False

    def isetvalues(self):
        DONE = False
        while not DONE:
            idx = raw_input("Set value for which index? [q to quit] ")
            if idx == 'q':
                break
            val = raw_input("What value? ")
            self[int(idx)] = val

    def policy(self):
        options = self.empty_cells
        player_moves = self.findall(self.player)

        win = self.winnable(self.auto)
        if win is not False:
            return win
        block = self.winnable(self.player)
        if block is not False:
            return block
        if len(options) == 8:
            #first round, second turn
            pm = player_moves.next()
            # if first move was in corner, hit the middle
            if pm != 4:
                return 4
            return random.choice(self.emptycorners())
        if len(options) == 6:
            if len(self.emptycorners()) == len(self.emptyedges()) == 3:
                l = [self.l2g(i) for i in self.findall(self.player)]
                for c in self.emptycorners():
                    coord_auto = self.l2g(c)
                    if all([(i in j) for i, j in zip(coord_auto, zip(*l))]):
                        return c
            return random.choice(self.emptycorners())

        # computer goes first:
        elif len(options) in (9, 7, 5):
            if len(options) == 7:
                p = player_moves.next()
                if not self.iscorner(p):
                    for c in self.emptycorners():
                        coord_auto = self.l2g(c)
                        coord_player = self.l2g(p)
                        if coord_auto[0] == coord_player[0] or \
                            coord_auto[1] == coord_player[1]:
                            return c
            return random.choice(self.emptycorners())
        else:
            try:
                return random.choice(self.emptyedges())
            except IndexError:
                return random.choice(tuple(options))

    def gameover(self, sym=x):
        """Returns False if not gameover, True if draw, else returns the winning
        symbol.
        """
        if self.won(sym):
            return sym
        elif len(self.empty_cells) == 0:
            return True
        else:
            return False

    def turn(self, auto=False, demo=None):
        sym = self.auto if auto else self.player
        if not auto:
            print demo or ''
            print ''
            idx = raw_input("Where do you want to move? Choose number as shown \
above. ")
        else:
            idx = self.policy()
        self[int(idx)] = sym
        demo[int(idx)] = ' '
        if auto:
            print self
            print ''
        return self.gameover(sym)

def main():
    auto_first = raw_input("Do you want to go first? [y/n] ").lower()[0] == 'n'
    # print auto_first
    demo, b = Board(), Board(x, o)
    demo.setboard()
    DONE = False
    whose_turn = cycle([auto_first, not auto_first])
    while not DONE:
        DONE = b.turn(auto=next(whose_turn), demo=demo)
    print b
    if DONE == True:
        print 'Game over! Draw!'
    else:
        print "Game over! %s's one!" % DONE

    # idx = raw_input('Choose a square by the number as shown above. ')

if __name__ == '__main__':
    pass
    main()