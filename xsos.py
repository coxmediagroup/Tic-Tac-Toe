from __future__ import division
import math
import random
import pdb
"""
http://chessprogramming.wikispaces.com/Negamax
int negaMax( int depth ) {
    if ( depth == 0 ) return evaluate();
    int max = -oo;
    for ( all moves)  {
        score = -negaMax( depth - 1 );
        if( score > max )
            max = score;
    }
    return max;
}
"""

class Grid(object):
    """
    A simple class for playing X's & O's (tic tac toe).
    """
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
    
    def _swap(self, value):
        """
        Swaps a given mark with the nmax value. ie 2 = -1
        """
        if value == -1: value = 2
        elif value == 2: value = -1
        return value
    
    def _swap_grid(self, grid):
        """
        Returns a copy of grid with values swapped by self._swap.
        """
        print "swapping grid"
        print grid
        swapped = [map(self._swap, grid[r]) for r in range(self.size)]
        print swapped
        return swapped
    
    
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
    
    def _check_grid(self, grid, row, col, mark, alpha=1, beta=-1):
        """
        Checks a series of positions and returns their "score".
        """
        rng = range(self.size)
        grid[row][col] = mark
        check_grid = self._swap_grid(grid)
        go, winner = self.game_over(grid=check_grid, set_winner=False)
        if not winner or winner == self.cat:
            winner = 0
        else:
            winner = self.marks[winner]
        winner = self._swap(winner)
        print "winner, mark",winner,mark
        if go and winner == mark:
            #grid[row][col] = 0
            #return mark
            return self._swap(winner)
        else:
            for r in rng:
                for c in rng:
                    if not grid[r][c]:
                        score = -self._check_grid(grid, r, c, mark, -beta, -alpha)
                        print "score, alpha, beta", score, alpha, beta
                        if score < alpha:
                            alpha = score
                            if score <= beta:
                                break
            #grid[row][col] = 0
            return alpha

    def _negamax(self, mark):
        """
        Returns an optimized move.
        """
        # deep copy...
        grid = [list(x) for x in self.grid]
        value = -1
        moves = []
        rng = range(self.size)
        for r in rng:
            for c in rng:
                if not grid[r][c]:
                    score = self._check_grid(self._swap_grid(grid),r,c,self._swap(mark))
                    print "score, value",score, value
                    if score > value:
                        value = score
                        moves = [(r,c)]
                        print "found a good move!"
                        print moves
                    elif score == value:
                        print "found a move!"
                        moves.append((r,c))
                        print moves
        return random.choice(moves)
    
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
        r,c = self._negamax(mark)
        self.grid[r][c] = mark
    
    def move(self, mark):
        """
        Completes a move for the given mark automatically.
        """
        def find_side(r,c):
            sides = ((r-1,c-1),(r+1,c+1),(r-1,c+1),(r+1,c-1),)
            for sr,sc in sides:
                try:
                    if not self.grid[sr][sc]:
                        return (sr, sc)
                except IndexError:
                    pass
            return None
        opmark = 1 if mark == 2 else 2
        size = self.size
        s = size - 1
        corners = ((0,0),(s,s),(0,s),(s,0))
        # see if we need to block
        block = self._find_major_row(opmark)
        if block:
            self.grid[block[0]][block[1]] = mark
            return
        # see if we have 2 in a row to complete
        best = self._find_major_row(mark)
        if best:
            self.grid[best[0]][best[1]] = mark
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
        r,c = self._negamax(mark)
        self.grid[r][c] = mark
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
    
    