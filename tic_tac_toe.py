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

    def __repr__(self):
        return self.board_str % tuple(self.grid)
        