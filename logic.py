class Board(object):
    """
    This class represents a basic game board. The cells will hold either X or O, or None
    if a player has not played it yet.
    """
    def __init__(self):
        self.cells = []
        for i in range(0, 3):
            self.cells.append([None]*3)
        

    def output(self):
        for row in self.cells:
            for cell in row:
                print cell, ' ', 
            print '\n'

    def get_val(self, x, y):
        return self.cells[y][x]

    def set_val(self, x, y, val):
        self.cells[y][x] = val

class Player(object):
    """
    Base class for either human or computer based player.
    """
    def __init__(self, board):
        self.board = board

    def get_move(self):
        """Returns a tuple of board coordinates (x,y)"""
        pass


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

def main():
    b = Board()
    p1 = None
    p2 = None
    g = Game(b, p1, p2)
    print g._build_row_ranges()
    

if __name__ == '__main__':
    main()


