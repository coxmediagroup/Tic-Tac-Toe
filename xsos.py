from __future__ import division
import math
import random
import pdb

class Grid(object):
    """
    A simple class for playing X's & O's (tic tac toe).
    """
    # infinity constants
    oo = float("inf")
    noo = -float("inf")
    # marks as constants
    X = 1
    O = 2
    # marks as dict
    marks = {
        'X':1,
        'O':2,
        '1':'X',
        '2':'O'
    }
    players = ('X', 'O')
    cat = 'Cat'
    grid = []
    # size of the grid
    size = None
    # str representation of the winner. Will be X, O, or Cat
    winner = ''
    # list of players the computer should play for
    comp_players = []
    
    def _op(self, value):
        """
        Returns the opposite value.
        1 -> 2
        2 -> 1
        0 -> 0
        """
        if value == 1:
            return 2
        elif value == 2:
            return 1
        else:
            return value
    
    def _op_grid(self, grid):
        """
        Returns a copy of grid with opposite values as evaluated by self._op.
        """
        return [map(self._op, r) for r in grid]
    
    def __init__(self, size=3):
        """
        Constructs a square grid of the given size (3 by default).
        """
        self.size = size
        self._create_grid()
    
    def _create_grid(self):
        """
        Creates the playing grid from self.size in self.grid.  Will desctruct
        an existing grid.
        
        Returns None.
        """
        grid = []
        size = self.size
        rng = range(size)
        for i in rng:
            row = [0]*size
            grid.append(row)
        self.grid = grid
    
    def _get_rotated_grid(self, grid=None):
        """
        Returns self.grid rotated 90 degrees so columns become rows.
        
        See http://mail.python.org/pipermail/tutor/2006-November/051039.html
        """
        if not grid: grid = self.grid
        size = self.size
        return [[grid[col][size-row-1] for col in range(size)] for row in range(size)]
    
    def _get_diagonal_rows(self, grid=None):
        """
        Returns the 2 diagonal rows in a list with the top left to bottom right
        first.
        """
        if not grid: grid = self.grid
        size = self.size
        rng = range(size)
        return [[grid[x][x] for x in rng], [grid[x][size-x-1] for x in rng]]
    
    def _get_all_rows(self, grid=None):
        """
        Returns the grid with the addition of columns and diagonals as rows.
        """
        if not grid: grid = self.grid
        return grid + self._get_rotated_grid(grid=grid) + self._get_diagonal_rows(grid=grid)
    
    def _get_moves(self):
        l = []
        rng = range(self.size)
        for r in rng:
            for c in rng:
                l.append((r,c))
        return l
    
    def _get_pretty_print_grid(self, grid=None):
        """
        Returns a string representing the current playing grid.
        """
        if not grid: grid = self.grid
        s = ''
        size = self.size
        rng = range(size)
        for i in rng:
            r = grid[i]
            for c in rng:
                if r[c]:
                    s += " %s " % self.marks[str(r[c])]
                else:
                    s += "   "
                if c+1 < size:
                    s += "|"
            if i+1 < size:
                s += "\n"
                s += "---+" * (size-1)
                s += "---\n"
        return s
    
    def _find_major_row(self, mark):
        """
        Looks for self.size-1 (two in a row for standard tic tac toe) of the
        given mark in a row and returns the grid position of the open space as
        a tuple (row, col)
        """
        size = self.size
        rng = range(size)
        rgrid = self._get_rotated_grid()
        diags = self._get_diagonal_rows()
        for r in rng:
            if self.grid[r].count(mark) >= size-1 and 0 in self.grid[r]:
                return (r, self.grid[r].index(0))
            if rgrid[r].count(mark) >= size-1 and 0 in rgrid[r]:
                return (rgrid[r].index(0), size-1-r)
        for r in range(len(diags)):
            # backwards diag first
            if diags[r].count(mark) >= size-1 and 0 in diags[r]:
                idx = diags[r].index(0)
                if not r:
                    return (idx, idx)
                else:
                    return (idx, size-1-idx)

    def _negamax(self, grid, mark, row, col, depth, alpha, beta, max_depth=10):
        """
        Negamax algorithm to explore best game moves.
        """
        max = None
        pair = None
        # deep copy
        grid2 = [list(x) for x in grid]
        # is the move being analyzed legal?
        if not grid2[row][col]:
            grid2[row][col] = mark
            go, winner = self.game_over(grid=grid2, set_winner=False)
            # is the game over?
            if go or depth > max_depth:
                # who won?
                if not winner:
                    return -1, (row,col)
                if winner == self.cat:
                    return 0, (row,col)
                else:
                    winner = self.marks[winner]
                if winner == mark:
                    return 1, (row,col)
                else:
                    return 0, (row,col)
            else:
                # better try some other permutations
                max = -1
                rr, rc = row, col
                rng = range(self.size)
                for r in rng:
                    for c in rng:
                        opmark = self._op(mark)
                        opgrid = self._op_grid(grid2)
                        x, pair = self._negamax(opgrid, opmark, r, c, depth+1, -beta, -alpha, max_depth=max_depth)
                        if x is None and pair is None: continue
                        x = -x
                        if x > max:
                            max = x
                        if x > alpha:
                            alpha = x
                        if alpha >= beta:
                            return alpha, pair
        return max, pair
    
    def _negamax2(self, grid, mark, depth, alpha, beta, max_depth=10):
        """
        Negamax algorithm to explore best game moves.
        """
        # deep copy
        grid2 = [list(x) for x in grid]
        go, winner = self.game_over(grid=grid2, set_winner=False)
        if go or depth > max_depth:
            if winner == self.cat:
                return 0
            winner = self.marks[winner]
            if winner == mark:
                return 1
            else:
                return -1
        # better try some other permutations
        max = -10
        rng = range(self.size)
        for r in rng:
            for c in rng:
                if not grid2[r][c]:
                    opmark = self._op(mark)
                    grid2[r][c] = opmark
                    opgrid = self._op_grid(grid2)
                    x = -self._negamax2(grid2, mark, depth+1, -beta, -alpha, max_depth=max_depth)
                    if x > max:
                        max = x
                    if x > alpha:
                        alpha = x
                    if alpha >= beta:
                        max = alpha
        return max
    
    
    
    def game_over(self, grid=None, set_winner=True):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        if not grid: grid = self.grid
        winner = ''
        size = self.size
        all_rows = self._get_all_rows(grid=grid)
        if '0' not in str(all_rows):
            winner = self.cat
            if set_winner:
                self.winner = winner
            return True, winner
        for r in all_rows:
            # only check rows that are full
            s = sum(r)
            if 0 not in r and not s%size:
                winner = self.marks[str(int(s/size))]
                if set_winner:
                    self.winner = winner
                return True, winner
        if set_winner:
            self.winner = winner
        return False, winner
    
    def move_nmax(self, mark):
        max = -1
        pairs = []
        rng = range(self.size)
        for r in rng:
            for c in rng:
                if not self.grid[r][c]:
                    self.grid[r][c] = mark
                    print "scoring", self._get_pretty_print_grid()
                    score = self._negamax2(self.grid,mark,0,1,-1)
                    print score, max
                    if score > max:
                        max = score
                        pairs = [(r,c)]
                    elif score == max:
                        pairs.append((r,c))
                    self.grid[r][c] = 0
        print pairs
        pair = random.choice(pairs)
        self.grid[pair[0]][pair[1]] = mark
    
    def move(self, mark):
        """
        Completes a move for the given mark automatically.
        """
        def find_side(r,c):
            sides = ((r-1,c),(r+1,c),(r,c+1),(r,c-1),)
            for sr,sc in sides:
                if sr < 0 or sc < 0: continue
                try:
                    if not self.grid[sr][sc]:
                        return (sr, sc)
                except IndexError:
                    continue
            return None
        opmark = self._op(mark)
        size = self.size
        s = size - 1
        corners = ((0,0),(s,s),(0,s),(s,0))
        # see if we have 2 in a row to complete
        best = self._find_major_row(mark)
        if best:
            self.grid[best[0]][best[1]] = mark
            return
        # see if we need to block
        block = self._find_major_row(opmark)
        if block:
            self.grid[block[0]][block[1]] = mark
            return
        # center is a great place to start
        if size % 2:
            mid = int(math.ceil(self.size/2)-1)
            if not self.grid[mid][mid]:
                self.grid[mid][mid] = mark
                return
        # watch the sides next to taken corners tho
        for r,c in corners:
            corner = self.grid[r][c]
            if corner:
                if corner == opmark:
                    side = find_side(r, c)
                    if side:
                        self.grid[side[0]][side[1]] = mark
                        return
        # corners are a good defense
        # check for corners that could be forks...
        for r,c in corners:
            if not self.grid[r][c]:
                side = find_side(r,c)
                if not side:
                    self.grid[r][c] = mark
                    return
        for r,c in corners:
            if not self.grid[r][c]:
                self.grid[r][c] = mark
                return
        # take a random open position
        #moves = self._get_moves()
        #while moves:
        #    r, c = moves.pop(random.randrange(len(moves)))
        #    if not self.grid[r][c]:
        #        self.grid[r][c] = mark
        #        return
        self.move_nmax(mark)
        return
    
    def autoplay(self):
        over = self.game_over()
        while not over:
            for p in self.players:
                self.move(self.marks[p])
                over = self.game_over()
                if over:
                    break
    
    def reset(self):
        """
        Resets the current winner, computer players & the grid.
        """
        self.comp_players = []
        self.winner = ''
        self._create_grid()
    
    def play(self):
        """
        Plays the game of tic tac toe.
        """
        over, winner = self.game_over()
        rng = range(self.size)
        while not over:
            for p in self.players:
                mark = getattr(self, p)
                print("Player %s is up!" % p)
                print("Current Grid:")
                print(self._get_pretty_print_grid())
                if p not in self.comp_players:
                    valid_cell = False
                    while not valid_cell:
                        print "Please choose an open cell to place your mark"
                        r = -1
                        while r not in rng:
                            i = raw_input("Please select a row (1-%s): " % str(self.size))
                            try:
                                r = int(i) - 1
                            except:
                                print "Please enter a valid choice."
                                continue
                        c = -1
                        while c not in rng:
                            i = raw_input("Please select a column (1-%s): " % str(self.size))
                            try:
                                c = int(i) - 1
                            except:
                                print "Please enter a valid choice."
                                continue
                        valid_cell = not self.grid[r][c]
                    self.grid[r][c] = mark
                else:
                    self.move(mark)
                over, winner = self.game_over()
                if over:
                    break
        print("The game is over. %s won!" % self.winner)
        print(self._get_pretty_print_grid())
    
    def start_game(self, welcome=True):
        """
        Resets and then sets up the players for a new game.
        """
        self.reset()
        if welcome:
            print("Welcome to X's & O's!")
        cx = ''
        while not cx:
            cx = raw_input("Do you want the computer to play for X? [y or n] ")
        if cx.lower().startswith('y'):
            self.comp_players.append('X')
        co = ''
        while not co:
            co = raw_input("Do you want the computer to play for O? [y or n] ")
        if co.lower().startswith('y'):
            self.comp_players.append('O')
        self.play()
        again = raw_input("Would you like to play again? [y or n] ")
        if not again.startswith('y'):
            print("Good bye!")
        else:
            self.start_game(welcome=False)

if __name__ == '__main__':
    g = Grid()
    g.start_game()
    
    