
import sys
from copy import deepcopy

# Constants
BOARD_ROWS = 3
BOARD_COLS = 3
MARK_CROSS = 'X'
MARK_CIRCLE = 'O'
MARK_EMPTY = None

class Board:
    """ Game Board """

    def __init__(self, cells=None):
        # load
        self.cells = cells

        # create if None
        # NOTE: cells are in cells[ROW][COL] format!
        if self.cells is None:
            self.cells = [ ]
            for r in range(BOARD_ROWS):
                row = [ ]
                for c in range(BOARD_COLS):
                    row.append(MARK_EMPTY)
                self.cells.append(row)

    def in_range(self, row, col):
        """ Check if a cell is in range / cordinates are correct """
        return col < BOARD_COLS and row < BOARD_ROWS

    def is_free(self, row, col):
        """ Checks if a cell on board is free """
        return self.in_range(col=col, row=row) and self.cells[row][col] == MARK_EMPTY

    def mark(self, row, col, mark):
        """ Mark a cell as taken w/ mark """
        # check if free first
        if not self.is_free(col=col, row=row):
            return False

        # mark it
        self.cells[row][col] = mark
        return True

    def clear_mark(self, row, col):
        """ clears the cells mark """
        self.cells[row][col] = MARK_EMPTY

    def cell_class(self, row, col):
        """ returns the cells with values as classes for use in template """
        if not self.in_range(row=row, col=col):
            return MARK_EMPTY
        
        # store cell
        cell = self.cells[row][col]

        # fontawesome class mark
        if cell == MARK_CROSS:
            return 'fa-times'
        elif cell == MARK_CIRCLE:
            return 'fa-circle-o'
        return ''

    def cell(self, row, col):
        """ returns the value for a cell
        :warning: does not check cell boundaries
        :return: cell value
        """
        return self.cells[row][col]

    @property
    def possible_moves(self):
        """ generate a list of dictionaries w/ all possible moves left
        :return: a list of dict w/ keys (row, col) of possible moves
        """
        moves = [ ]
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.is_free(row=row, col=col):
                    moves.append(dict(row=row, col=col))
        return moves

    def to_dict(self):
        """ Save the session to a dictionary """
        return { 'cells': deepcopy(self.cells) }

    @classmethod
    def from_dict(cls, state):
        """ Load the board state from a dictionary """
        cells = deepcopy(state['cells']) if 'cells' in state else [ ]
        return cls(cells=cells)

    def clone(self):
        """ returns a cloned deepcopy of the board
        :return: a deepcopy of the board
        """
        return Board.from_dict(self.to_dict())

class GameEngine:
    """ TicTacToe game engine """
    def __init__(self, board=None, user_mark=MARK_CROSS):
        # construct a game board if None
        self.board = Board() if not board else board
        self.user_mark = user_mark if user_mark else MARK_CROSS

    @property
    def engine_mark(self):
        """ returns the mark used by the engine """
        return MARK_CIRCLE if self.user_mark == MARK_CROSS else MARK_CROSS

    def is_free(self, col, row):
        """ Check if a cell is free
        :return: True if empty / free
        """
        return self.board.is_free(col=col, row=row)

    def mark(self, col, row, mark):
        """ mark a cell as taken by mark
        :return: True if mark was successfully set
        """
        return self.board.mark(col=col, row=row, mark=mark)

    def mark_player(self, col, row):
        """ mark a cell as taken by the user
        :return: True if the mark was successfully set
        """
        return self.mark(col=col, row=row, mark=self.user_mark)

    def mark_engine(self, col, row):
        """ mark a cell as taken by the game engine
        :return: True if the mark was successfully set
        """
        return self.mark(col=col, row=row, mark=self.engine_mark)

    def line_score(self, cell1, cell2, cell3):
        """ Compares the current board and calculates a score

        :return: a calculated score for line
        """
        score = 0

        # first cell
        if self.board.cell(**cell1) == self.engine_mark: # mine
            score = 1
        elif self.board.cell(**cell1) == self.user_mark: # opp
            score = -1

        # second cell
        if self.board.cell(**cell2) == self.engine_mark: # mine
            if score == -1: # we cancel out
                return 0
            score = 10 if score == 1 else 1 # 10 points if I own cell 1 too else just 1 point
        elif self.board.cell(**cell2) == self.user_mark: # opp
            if score == 1: # we cancel out
                return 0
            score = -10 if score == -1 else -1 # -10 points if they own cell 1 too else just -1 point

        # third cell
        if self.board.cell(**cell3) == self.engine_mark: # mine
            if score < 0: # they own cell1 and / or cell2
                return 0
            score = 100 if score > 0 else 1 # I own two else I own one, rest empty
        elif self.board.cell(**cell3) == self.user_mark: # opp
            if score > 0: # I own cell1 and / or cell2
                return 0
            score = -100 if score < 0 else -1 # They own two else I own one, rest empty

        return score

    @property
    def best_score(self):
        """ returns the best possible score for the board
        
        Complete winning combo (horizontal, veritical, diagonal) is +100 points, losing is -100
        Partial winning combo w/ 1 square missing is +10, losing -10
        Partial winning combo w/ 2 squares missing is +1, losing -1

        :return: best possible score for board (integer)
        """
        score = 0

        # add diagonals
        score += self.line_score({ 'row': 0, 'col': 0 }, { 'row': 1, 'col': 1 }, { 'row': 2, 'col': 2 }) # \ <-- direction
        score += self.line_score({ 'row': 2, 'col': 0 }, { 'row': 1, 'col': 1 }, { 'row': 0, 'col': 2 }) # / <-- direction

        # add horizontals and verticals
        for i in range(BOARD_COLS):
            score += self.line_score({ 'row': i, 'col': 0 }, { 'row': i, 'col': 1 }, { 'row': i, 'col': 2 }) # horizontal
            score += self.line_score({ 'row': 0, 'col': i }, { 'row': 1, 'col': i }, { 'row': 2, 'col': i }) # vertical

        return score

    def calc_next(self, mark=None, depth=2):
        """ calculates the next best move to be made and returns a dict with row and col
        Implements the minimax algorithm (recursive)

        Source: http://www.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html
        
        :param level: recrusive node depth
        :param mark: mark to be used for this iteration
        :return: a dictionary with row and col keys
        """
        # generate params
        mark = self.engine_mark if not mark else mark
        possible_moves = self.board.possible_moves
        best_score = (-sys.maxint - 1) if mark == self.engine_mark else sys.maxint 

        if not possible_moves or depth <= 0:
            return { 'best_score': self.best_score }

        # bruteforce through all possible moves and see which one is the best
        for move in possible_moves:
            # try this move for current_mark
            self.board.mark(mark=mark, row=move['row'], col=move['col'])

            # check if this was the best move
            if mark == self.engine_mark: # best move for me (computer)
                current_score = self.calc_next(mark=self.user_mark, depth=depth - 1)['best_score']
                if current_score > best_score: # greater than max negative
                    best_score = current_score
                    best_move = move

            else: # best move for other player (human (hopefully))
                current_score = self.calc_next(mark=self.engine_mark, depth=depth - 1)['best_score']
                if current_score < best_score: # greater than max positive
                    best_score = current_score
                    best_move = move
            
            # undo move
            self.board.clear_mark(row=move['row'], col=move['col'])

        return { 'best_score': best_score,
                'row': best_move['row'],
                'col': best_move['col'] }

    def move_next(self):
        """ calculates the next best move to be made and sets a mark there
        :return: True if the mark was successfully set
        """
        # Skip if gameover
        if self.gameover:
            return False

        # get best move
        best_move = self.calc_next(mark=self.engine_mark)

        # set mark
        if best_move:
            return self.mark_engine(row=best_move['row'], col=best_move['col'])

        return False

    def check_line(self, cell1, cell2, cell3):
        """ checks if the current line is complete and won by engine
        :return: True if the engine won, False if not won, None if line incomplete
        """
        if self.board.cell(**cell1) == self.engine_mark \
            and self.board.cell(**cell2) == self.engine_mark \
            and self.board.cell(**cell3) == self.engine_mark:
                return True
        elif self.board.cell(**cell1) == self.user_mark \
            and self.board.cell(**cell2) == self.user_mark \
            and self.board.cell(**cell3) == self.user_mark:
                return False

        return None

    @property
    def engine_won(self):
        """ checks if the engine won
        :return: True if the engine won, False if not won, None if draw or gameover
        """
        win_combos = [ ]

        # diagonals
        win_combos.append([{ 'row': 0, 'col': 0 }, { 'row': 1, 'col': 1 }, { 'row': 2, 'col': 2 }]) # \ <-- direction
        win_combos.append([{ 'row': 2, 'col': 0 }, { 'row': 1, 'col': 1 }, { 'row': 0, 'col': 2 }]) # / <-- direction

        # horizontals and verticals
        for i in range(BOARD_COLS):
            win_combos.append([{ 'row': i, 'col': 0 }, { 'row': i, 'col': 1 }, { 'row': i, 'col': 2 }]) # horizontal
            win_combos.append([{ 'row': 0, 'col': i }, { 'row': 1, 'col': i }, { 'row': 2, 'col': i }]) # vertical

        # check combos
        for combo in win_combos:
            won = self.check_line(*combo)
            if not won is None: # we either lost or won
                return won

        return None

    @property
    def gameover(self):
        """ Checks if the game is over
        :return: True if the game is over / all marks are set
        """
        return not self.board.possible_moves or not self.engine_won is None

    def to_dict(self):
        """ Save the game engine state to dictionary """
        return {
            'board': self.board.to_dict(),
            'user_mark': self.user_mark
        }

    @classmethod
    def from_dict(cls, state):
        """ Load the game engine from a dictionary """
        board = Board.from_dict(state['board']) if 'board' in state else Board()
        user_mark = state['user_mark'] if 'user_mark' in state else None
        return cls(board=board, user_mark=user_mark)

