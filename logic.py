class Board(object):
    """
    This class represents a basic game board. The cells will hold either X or O, or None
    if a player has not played it yet.
    """
    def __init__(self):
        self._move_cache = None
        self._cells = []
        for i in range(0, 3):
            self._cells.append([None]*3)
        

    def output(self):
        for row in self._cells:
            for cell in row:
                if cell is None: 
                    print '%02s'%'-',
                else:
                    print '%02s'%cell,
            print '\n'

    def get_val(self, x, y):
        return self._cells[y][x]

    def set_val(self, x, y, val):
        self._move_cache = None
        self._cells[y][x] = val

    def get_valid_moves(self):
        """
        Returns a list of valid moves left (without an X or an O in them)
        Will not compute itself twice without a set_val
        """
        if self._move_cache:
            return self._move_cache

        out = []
        for y, row in enumerate(self._cells):
            for x, cell in enumerate(row):
                if cell == None:
                    out.append((x, y))
        self._move_cache = out
        return out

class Player(object):
    """
    Base class for either human or computer based player.
    """
    def __init__(self, board, avatar=None):
        self.board = board
        self.avatar = avatar

    def get_move(self):
        """
        Returns a tuple of board coordinates (x,y)
        This is a very simple implementation to be overwritten by child classes
        """
        print "Please enter coordinates for a move in form of (x, y) for %s"%self.avatar
        try:
            move = eval(raw_input())
        except:
            print "Invalid input"
            return get_move()

        if move not in self.board.get_valid_moves() or not isinstance(move, tuple):
            print "Invalid move"
            return self.get_move()
        return move

class Game(object):
    """ 
    X(horizontal)/Y(vertical) Coordinates
      0   1   2
    0 X | X | X
    1 X | X | X
    2 X | X | X

    Row designations 
    6 3   4   5 7
    0 X | X | X
    1 X | X | X    
    2 X | X | X
    """

    def __init__(self, board, p1, p2):
        self.board = board
        self.p1 = p1
        self.p2 = p2
        self.turn = 1
        self._ranges = self._build_row_ranges()

    def _get_row(self, row_number):
        return [self.board.get_val(*cell) for cell in self._ranges[row_number]]

    def _check_row_for_win(self, row):
        vals = [self.board.get_val(*cell) for cell in row]
        if vals == ['X']*3: return 'X'
        elif vals == ['O']*3: return 'O'
        return False
        
    def _build_row_ranges(self):
        #horizontal rows
        rows = {}
        for y in range(0,3):
            row = []
            for x in range(0,3):
                row.append((x,y))
            rows[y] = row

        #vertical rows
        for x in range(0,3):
            row_n = x + 3
            row = []
            for y in range(0, 3):
                row.append((x,y))
            rows[row_n] = row

        #diagonals
        for i in range(0,3):
            rows.setdefault(6, []).append((i,i))
            rows.setdefault(7, []).append((2-i, i))
        return rows

    def check_for_win(self):
        """Checks the board for a win. (via every possible row)"""
        for number, row in self._ranges.iteritems():
            win = self._check_row_for_win(row)
            if win:
                return (number, win)
        return False

    def start(self):
        while True:
            self.board.output()
            p = self.p1 if self.turn == 1 else self.p2
            avatar = 'X' if self.turn == 1 else 'O'
            move = p.get_move()
            self.board.set_val(move[0], move[1], avatar)
            win = self.check_for_win()
            if win:
                print "Player %d (%s's) won on row %d!"%(self.turn, avatar, win[0])
                return win
            if not self.board.get_valid_moves():
                print "Tie."
                return None

            self.turn = 2 if self.turn == 1 else 1

def main():
    b = Board()
    p1 = None
    p2 = None
    g = Game(b, Player(b, 'X'), Player(b, 'O'))
    g.start()
    

if __name__ == '__main__':
    main()


