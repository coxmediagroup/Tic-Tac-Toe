def print_grid(li_grid):
    rstr =  "+-+-+-+\n"
    for row in li_grid:
        rstr += "|"
        for col in row:
            if col == None:
                col = "-"
            rstr += str(col) + "|"
        rstr += "\n"
    rstr += "+-+-+-+\n"
    print rstr


class PlayException(Exception):
    """You're cheating!"""


class EndGameException(Exception):
    """Game over dude"""


class Board(object):
    """Represents a basic tic-tac-toe board"""

    def __init__(self):
        self.li_grid = [[None] * 3 for x in range(3)]

    def play(self, marker, row, col):
        """places marker on the board"""
        cur_val = self.li_grid[row][col]
        if cur_val != None:
            raise PlayException()
        self.li_grid[row][col] = marker


class Player(object):
    """ abstract class that represents a Player"""

    def __init__(self, board, marker, other_marker):
        self.board = board
        self.marker = marker
        self.other_marker = other_marker

    def _available_moves_(self):
        li_moves = []
        for row in range(3):
            for col in range(3):
                if self.board.li_grid[row][col] == None:
                    li_moves.append([row, col])
        return li_moves




class AIPlayer(Player):

    def take_your_turn(self):
        available_moves = self._available_moves_()
        if not available_moves:
            raise EndGameException("I Quit!")
        best_move = None
        best_score = 0
        for row, col in available_moves:
            score = self._score_move_(row, col)
            if score > best_score:
                best_score = score
                best_move = [row, col]
        if best_move:
            self.board.play(self.marker, best_move[0], best_move[1])
        else:
            self.board.play(self.marker, available_moves[0][0], available_moves[0][1])

    def _score_move_(self, row, col):
        """
        1 point for every possible series
        1 more point for every marker already in series
        1 point for every possible block
        """
        score = 0

        #score up and down
        row_series = self.board.li_grid[row]
        score += self._score_series_(row_series)
        col_series = [arow[col] for arow in self.board.li_grid]
        score += self._score_series_(col_series)

        if (row == 1 and col != 1) or (col == 1 and row != 1):
            return score #no diags

        #score across
        across_ur_lr = [(0, 0), (1, 1), (2, 2)]
        across_lr_ur = [(2, 0), (1, 1), (0, 2)]

        if (row, col) in across_ur_lr:
            series = [self.board.li_grid[x[0]][x[1]] for x in across_ur_lr]
            score += self._score_series_(series)

        if (row, col) in across_lr_ur:
            series = [self.board.li_grid[x[0]][x[1]] for x in across_lr_ur]
            score += self._score_series_(series)

        return score

    def _score_series_(self, li_series):
        if self.other_marker in li_series:
            #blocked by other player
            if not self.marker in li_series:
                #uh oh, maybe I should block
                return 1 + sum([1 for x in li_series if x == self.other_marker])
            else:
                return 0
        else:
            score = 1
            return score + sum([1 for x in li_series if x == self.marker])


class Game(object):
    def __init__(self, pl1_class, pl2_class):
        self.board = Board()
        self.pl1 = pl1_class(self.board, "X", "O")
        self.pl2 = pl2_class(self.board, "O", "X")

    def _check_winner_(self):
        across_ur_lr = [(0, 0), (1, 1), (2, 2)]
        across_lr_ur = [(2, 0), (1, 1), (0, 2)]

        for p in ["X", "O"]:
            for x in range(3):
                row_series = self.board.li_grid[x]
                col_series = [arow[x] for arow in self.board.li_grid]
                diag1 = [self.board.li_grid[x[0]][x[1]] for x in across_ur_lr]
                diag2 = [self.board.li_grid[x[0]][x[1]] for x in across_lr_ur]
                for series in [row_series, col_series, diag1, diag2]:
                    if all([amark == p for amark in series]):
                        print "%s wins!!!" % p
                        sys.exit(0)

    def start(self):
        print print_grid(self.board.li_grid)
        while 1:
            self.pl1.take_your_turn()
            print print_grid(self.board.li_grid)
            self._check_winner_()
            self.pl2.take_your_turn()
            print print_grid(self.board.li_grid)
            self._check_winner_()
