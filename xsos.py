from __future__ import division
import math
import random
import pdb

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
        1:'X',
        2:'O'
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
    
    def _center(self, grid=None):
        """
        Returns the value of the center cell if one exists or None.
        """
        if not grid: grid = self.grid
        center = None
        if size % 2:
            mid = int(math.ceil(self.size/2)-1)
            center = grid[mid][mid]
        return center
    
    def _get_rotated_grid(self, grid=None):
        """
        Returns self.grid rotated 90 degrees so columns become rows.
        
        See http://mail.python.org/pipermail/tutor/2006-November/051039.html
        """
        if not grid: grid = self.grid
        size = self.size
        return [[grid[col][size-row-1] for col in range(size)] for row in \
            range(size)]
    
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
        return grid + self._get_rotated_grid(grid=grid) + \
        self._get_diagonal_rows(grid=grid)
    
    def _get_elles(self, grid=None):
        """
        Returns the border of the grid in groups of L's.
        """
        if not grid: grid = self.grid
        rows = grid
        cols = self._get_rotated_grid(grid=grid)
        max = self.size - 1
        corners = (
            ((rows[0], cols[0]), (0, 0)),
            ((rows[0], cols[max]), (0, max)),
            ((rows[max], cols[0]), (max, 0)),
            ((rows[max], cols[max]), (max, max)),
        )
        elles = []
        # prune
        for pair in corners:
            if pair[0][0] == pair[0][1]: continue
            if pair[0][0] == pair[0][1][::-1]: continue
            elles.append(pair)
        return elles
    
    def _get_moves(self):
        lst = []
        rng = range(self.size)
        for row in rng:
            for col in rng:
                lst.append((row, col))
        return lst
    
    def _get_pretty_print_grid(self, grid=None):
        """
        Returns a string representing the current playing grid.
        """
        if not grid: grid = self.grid
        ret = ''
        size = self.size
        rng = range(size)
        for i in rng:
            row = grid[i]
            for col in rng:
                if row[col]:
                    ret += " %s " % self.marks[row[col]]
                else:
                    ret += "   "
                if col+1 < size:
                    ret += "|"
            if i+1 < size:
                ret += "\n"
                ret += "---+" * (size-1)
                ret += "---\n"
        return ret
    
    def _find_major_row(self, mark, grid=None):
        """
        Looks for self.size-1 (two in a row for standard tic tac toe) of the
        given mark in a row and returns the grid position of the open space as
        a tuple (row, col)
        """
        grid = self.grid if not grid else grid
        size = self.size
        rng = range(size)
        rgrid = self._get_rotated_grid(grid=grid)
        diags = self._get_diagonal_rows(grid=grid)
        for row in rng:
            if grid[row].count(mark) >= size-1 and 0 in grid[row]:
                return (row, self.grid[row].index(0))
            if rgrid[row].count(mark) >= size-1 and 0 in rgrid[row]:
                return (rgrid[row].index(0), size-1-row)
        for row in range(len(diags)):
            # backwards diag first
            if diags[row].count(mark) >= size-1 and 0 in diags[row]:
                idx = diags[row].index(0)
                if not row:
                    return (idx, idx)
                else:
                    return (idx, size-1-idx)
    
    def _find_minor_rows_count(self, mark, grid=None):
        """
        Counts the number of full rows that the given mark has a minor position.
        Essentially a block.
        """
        grid = self.grid if not grid else grid
        opmark = self._op(mark)
        count = 0
        rows = self._get_all_rows(grid=grid)
        for r in rows:
            if r.count(opmark) >= self.size-1 and mark in r:
                count += 1
        return count
    
    def _negamax2(self, grid, mark, depth, alpha, beta, max_depth=10):
        """
        Negamax algorithm to explore best game moves.
        """
        # deep copy
        grid2 = [list(x) for x in grid]
        go, winner = self.game_over(grid=grid2, set_winner=False)
        if go:
            if winner == self.cat:
                return 0
            winner = self.marks[winner]
            if winner == mark:
                return 1
            else:
                return -1
        if depth > max_depth:
            winning = self.winning(mark, grid=grid2)
            if winning is not None:
                if winning:
                    return 1
                return -1
            return 0
            
        # better try some other permutations
        rng = range(self.size)
        for row in rng:
            for col in rng:
                if not grid2[row][col]:
                    opmark = self._op(mark)
                    grid2[row][col] = opmark
                    opgrid = self._op_grid(grid2)
                    x = -self._negamax2(grid2, opmark, depth+1, -beta, -alpha,
                                        max_depth=max_depth)
                    grid2[row][col] = 0
                    if x < alpha:
                        alpha = x
                        if x <= beta: break
        return alpha
    
    def winning(self, mark, grid=None):
        """
        Examines the grid and attempts to analyze if a mark is winning based on
        patterns. This assumes that the grid is current so that if both marks
        have 2 in a row the mark opposite the provided mark will be winning
        other wise the cat will be winning.
        
        Returns a boolean for the given mark or None if the cat is winning
        """
        grid = self.grid if not grid else grid
        opmark = self._op(mark)
        # the default result is cat
        result = None
        # make sure the game isn't over
        go, winner = self.game_over(grid=grid, set_winner=False)
        if go:
            if winner != self.cat:
                result = self.marks[winner] == mark
        else:
            # check patterns
            # 2 in a row
            mrow = self._find_major_row(mark, grid=grid)
            oprow = self._find_major_row(opmark, grid=grid)
            result = True if mrow and not oprow else None
            result = False if oprow else None
            if result is None:
                mcount = self._find_minor_rows_count(mark, grid=grid)
                opcount = self._find_minor_rows_count(opmark, grid=grid)
                if mcount > opcount:
                    result = True
                elif opcount > mcount:
                    result = False
            # TODO there's probably a lot more I could do here with corner
            # strategy...
        return result
    
    def game_over(self, grid=None, set_winner=True):
        """
        Checks to see if the game is over.
        
        Returns a boolean.
        """
        if not grid: grid = self.grid
        winner = ''
        size = self.size
        all_rows = self._get_all_rows(grid=grid)
        for row in all_rows:
            # only check rows that are full
            s = sum(row)
            if 0 not in row and not s%size:
                winner = self.marks[int(s/size)]
                if set_winner:
                    self.winner = winner
                return True, winner
        if '0' not in str(all_rows):
            winner = self.cat
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
        for row in rng:
            for col in rng:
                if not self.grid[row][col]:
                    self.grid[row][col] = mark
                    score = self._negamax2(self.grid, mark, 0, 1, 1, -1)
                    if score > max:
                        max = score
                        pairs = [(row, col)]
                    elif score == max:
                        pairs.append((row, col))
                    self.grid[row][col] = 0
        pair = random.choice(pairs)
        self.grid[pair[0]][pair[1]] = mark
    
    def move(self, mark):
        """
        Completes a move for the given mark automatically.
        """
        def find_side(row, col):
            sides = ((row-1, col), (row+1, col), (row, col+1), (row, col-1), )
            for siderow, sidecol in sides:
                if siderow < 0 or sidecol < 0: continue
                try:
                    if not self.grid[siderow][sidecol]:
                        return (siderow, sidecol)
                except IndexError:
                    continue
            return None
        
        opmark = self._op(mark)
        size = self.size
        s = size - 1
        corners = ((0, 0), (s, s), (0, s), (s, 0))
        # center is a great place to start
        if size % 2:
            mid = int(math.ceil(self.size/2)-1)
            if not self.grid[mid][mid]:
                self.grid[mid][mid] = mark
                return
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
        # watch the sides next to taken corners tho
        cnr1 = self.grid[corners[0][0]][corners[0][1]]
        cnr2 = self.grid[corners[1][0]][corners[1][1]]
        cnr3 = self.grid[corners[2][0]][corners[2][1]]
        cnr4 = self.grid[corners[3][0]][corners[3][1]]
        if (cnr1 == cnr2 and cnr1 != 0) or (cnr3 == cnr4 and cnr3 != 0):
            for row, col in corners:
                corner = self.grid[row][col]
                if corner:
                    if corner == opmark:
                        side = find_side(row, col)
                        if side:
                            self.grid[side[0]][side[1]] = mark
                            return
        # check L's (fork prevention)
        els = self._get_elles()
        for pair, idxs in els:
            row = pair[0]
            col = pair[1]
            if row.count(0) == 2 and col.count(0) == 2:
                if opmark in row and opmark in col:
                    rowcol = row.index(0)
                    self.grid[idxs[0]][rowcol] = mark
                    return
        # corners are a good defense
        # check for corners that could be forks...
        for row, col in corners:
            if not self.grid[row][col]:
                side = find_side(row, col)
                if not side:
                    self.grid[row][col] = mark
                    return
        for row, col in corners:
            if not self.grid[row][col]:
                self.grid[row][col] = mark
                return
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
            for plyr in self.players:
                mark = getattr(self, plyr)
                print("Player %s is up!" % plyr)
                print("Current Grid:")
                print(self._get_pretty_print_grid())
                if plyr not in self.comp_players:
                    valid_cell = False
                    while not valid_cell:
                        print "Please choose an open cell to place your mark"
                        row = -1
                        while row not in rng:
                            inpt = raw_input("Please select a row (1-%s): " \
                                          % str(self.size))
                            try:
                                row = int(inpt) - 1
                            except:
                                print "Please enter a valid choice."
                                continue
                        col = -1
                        while col not in rng:
                            inpt = raw_input("Please select a column (1-%s): " \
                                          % str(self.size))
                            try:
                                col = int(inpt) - 1
                            except:
                                print "Please enter a valid choice."
                                continue
                        valid_cell = not self.grid[row][col]
                    self.grid[row][col] = mark
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
        compx = ''
        while not compx:
            compx = raw_input("Do you want the computer to play for X? [y or n] ")
        if compx.lower().startswith('y'):
            self.comp_players.append('X')
        compo = ''
        while not compo:
            compo = raw_input("Do you want the computer to play for O? [y or n] ")
        if compo.lower().startswith('y'):
            self.comp_players.append('O')
        self.play()
        again = raw_input("Would you like to play again? [y or n] ")
        if not again.startswith('y'):
            print("Good bye!")
        else:
            self.start_game(welcome=False)

if __name__ == '__main__':
    grid = Grid()
    grid.start_game()
    
    
