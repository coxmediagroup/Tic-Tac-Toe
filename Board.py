import copy
import logging
import random

logging.basicConfig(filename='/tmp/tic-tac-toe.log',level=logging.DEBUG)

class BoardException(Exception):
    pass

class BoardSpace(object):
    """
    Attributes for a space in a game board

    1) player
    2) index value within game board
    3) if this space is part of a winning move

    """
    def __init__(self, **kwargs):
        self.player = kwargs['player'] # required
        self.board_index = int(kwargs['board_index']) # required
        self.winner = kwargs.get('winner', False) # optional
        self.last_move = kwargs.get('last_move', False) # optional

    def __str__(self):
        return self.player

class Board(object):
    """
    The game board

    """
    INFINITY = 999
    MIN_DIM = 3
    MAX_DIM = 16

    def __init__(self, **kwargs):

        self.node_counter = 0
        self.node_depth = 0

        # Board settings
        self.ROWS = kwargs.get('rows', 3)
        self.COLS = kwargs.get('cols', 3)

        # Game rules
        self.IN_A_ROW = kwargs.get('in_a_row', 3)

        # Players
        self.P0 = kwargs.get('p0', '-') # player null (blank spaces)
        self.P1 = kwargs.get('p1', 'X') # player one
        self.P2 = kwargs.get('p2', 'O') # player two
        self.P1_AI = kwargs.get('p1_ai', False) # player one AI or human
        self.P2_AI = kwargs.get('p2_ai', False) # player one AI or human
        self.this_player = kwargs.get('this_player', None)
        self.next_player = kwargs.get('next_player', None)

        # Score Board
        self.score_board = {
            self.P0: 0,
            self.P1: 0,
            self.P2: 0,
        }

        # Put a game board together
        self._sanity_check()
        self.board = self.new_board()

    def _sanity_check(self):
        """
        Basic sanity tests to make sure the game settings makes sense

        """
        # Test the rows and cols are the minimal size
        msg = '"{}" must be an integer larger than {} and smaller than {}.'
        if not int(self.ROWS) >= self.MIN_DIM <= self.MAX_DIM:
            row_msg = msg.format('rows', self.MIN_DIM, self.MAX_DIM)
            raise BoardException(row_msg)
        if not int(self.COLS) >= self.MIN_DIM <= self.MAX_DIM:
            row_msg = msg.format('cols', self.MIN_DIM, self.MAX_DIM)
            raise BoardException(row_msg)

        # Test that the width of the character for blanks and player is 1 wide
        if not len(self.P0) == 1:
            raise BoardException("Blank spaces must be one character wide")
        if not len(self.P1) == 1:
            raise BoardException("Player 1 must be one character wide")
        if not len(self.P2) == 1:
            raise BoardException("Player 1 must be one character wide")

        # Test that there arent any duplicated players or blank characters
        msg = '"{}" must be unique'
        if self.P0 in (self.P1, self.P2):
            raise BoardException(msg.format("Blank spaces"))
        if self.P1 in (self.P0, self.P2):
            raise BoardException(msg.format("Player 1"))
        if self.P2 in (self.P0, self.P1):
            raise BoardException(msg.format("Player 2"))

        return True

    def new_board(self):
        """
        Game board is represented as a 2 dimensional list of BoardSpaces

        """
        board = []
        counter = 1
        for x in range(self.ROWS):
            board.append([])
            for y in range(self.COLS):
                s = BoardSpace(player=self.P0, board_index=counter)
                board[-1].append(s)
                counter += 1
        return board

    def clear_board(self):
        """
        Clear the spaces of player moves, while keeping the player scores

        """
        self.node_counter = 0
        self.node_depth = 0
        self.board = self.new_board()

    def ai(self):
        """
        For whichever player is the "current" player, auto-play their move.

        """
        this_space = None

        # Choose random, if starting on empty board
        remaining_spaces = self.remaining_spaces()
        if len(remaining_spaces) == (self.COLS * self.ROWS):
            this_space = random.choice(remaining_spaces)

        # Or use minimax
        elif remaining_spaces:
            this_space = self._minimax()[-1]
            # logging.debug('best move is: {}'.format(this_space.board_index))

        # if this_space is None then there is no valid move and
        # an Error should be raised
        if this_space:
            return self.move_player(self.this_player, this_space.board_index)
        else:
            # AI can't place a move if no spaces are left!
            raise BoardException("No available spaces for ai to place!")

    def _minimax(self, max_turn=True):
        """
        Minimax algorithm with alpha-beta pruning

        """
        # establish who is max and who is min
        if max_turn:
            this_player = self.this_player
        else:
            this_player = self.next_player

        # Available spaces on board
        remaining_spaces = self.remaining_spaces()

        # board has a winner?
        if self.winning_space():
            point = 1
            if max_turn:
                v = -point
                a = v
                b = self.INFINITY
            else:
                v = point
                a = -self.INFINITY
                b = v
            # logging.debug('Pt:{}'.format(v))
            # logging.debug('*' * 30)
            return (v, a, b, None)

        # Draw        
        if len(remaining_spaces) == 0:
            if max_turn:
                v = 0
                a = 0
                b = -self.INFINITY
            else:
                v = 0
                a = self.INFINITY
                b = 0
            # logging.debug('Pt:{}'.format(v))
            # logging.debug('*' * 30)
            return (v, a, b, None)

        # player max moves
        if max_turn:
            v = -self.INFINITY
            a = -self.INFINITY
            b = self.INFINITY
            best_move = (v, a, b, None)
            for space in remaining_spaces:
                self.node_counter += 1
                # max: if v > alpha; alpha-cut
                if best_move[0] <= best_move[1]:
                    self.node_depth += 1
                    self._place_player(this_player, space.board_index)
                    value, alpha, beta = self._minimax(max_turn=False)[0:3]
                    self.node_depth -= 1
                    self._un_place_player(space.board_index)
                    if value > best_move[0]:
                        best_move = (value, alpha, beta, space)

        # player min moves
        else:
            v = self.INFINITY
            a = self.INFINITY
            b = -self.INFINITY
            best_move = (v, a, b, None)
            for space in remaining_spaces:
                self.node_counter += 1
                # min: if v < beta; beta-cut
                if best_move[0] >= best_move[2]:
                    self.node_depth += 1
                    self._place_player(this_player, space.board_index)
                    value, alpha, beta = self._minimax(max_turn=True)[0:3]
                    self.node_depth -= 1
                    self._un_place_player(space.board_index)
                    if value < best_move[0]:
                        best_move = (value, alpha, beta, space)

        # return the best move
        return best_move

    def remaining_spaces(self):
        """
        How many valid spaces are left on the board

        """
        these_spaces = []
        for row in self.board:
            for space in row:
                if space.player == self.P0:
                    these_spaces.append(space)
        return these_spaces

    def winning_space(self):
        """
        Check if the last placed move was a winning move, regardless of player

        """
        if self.player_win_round(self.P1, flag_winner=False):
            return True
        elif self.player_win_round(self.P2, flag_winner=False):
            return True
        else:
            return False

    def _check_rows(self, this_player, this_board):
        """
        All wins are check by rows, if vertical or diagonal then rotate the
        board first before checking rows.

        """
        winning_spaces = []
        for row in this_board:
            spaces_in_a_row = []
            for space in row:
                if space.player == this_player:
                    spaces_in_a_row.append(space)
                else:
                    spaces_in_a_row = []
            if len(spaces_in_a_row) >= self.IN_A_ROW:
                winning_spaces += spaces_in_a_row
        return winning_spaces

    def _vertical_rows(self):
        """
        convert vertical "columns" spaces into "rows" before checking for
        a winning move.

        board:
        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

        rotated:
        [(7, 4, 1),
         (8, 5, 2),
         (9, 6, 3)]

        """
        # rotate the board, then check rows
        rotated_board = zip(*self.board)
        return rotated_board

    def _diagonal_rows(self, reverse=False):
        """
        convert a "diagonal" spaces into "rows" before checking for a winning
        move.

        normal board:
        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

        converted to diagonal rows:
        [[1],
         [2, 4],
         [3, 5, 7],
         [6, 8],
         [9]]

        converted to diagonal (reversed):
        [[3],
         [2, 6],
         [1, 5, 9],
         [4, 8],
         [7]]

        """
        if reverse:
            pop_index = -1
        else:
            pop_index = 0

        # copy of board
        board_copy = [x[:] for x in self.board[:]]

        # build the board on diagonals to rows
        diagonal_board = []

        # iterate over the copied board collecting diagonal spaces
        counter = 1
        while counter < (len(board_copy) + len(board_copy[0])):
            new_row = []
            for row in range(counter):
                try:
                    if board_copy[row]:
                        new_row.append(board_copy[row].pop(pop_index))
                except IndexError:
                    pass
            counter += 1
            diagonal_board.append(new_row)

        # Done
        return diagonal_board

    def player_win_round(self, this_player, flag_winner=True):
        """
        Game is won if player has N-in-a-row spots filled X times

        player = self.P1 or self.P2

        """
        winning_spaces = []

        # Check all rows
        these_spaces = self._check_rows(this_player, self.board)
        winning_spaces = list(set(winning_spaces + these_spaces))

        # Check columns
        this_board = self._vertical_rows()
        these_spaces = self._check_rows(this_player, this_board)
        winning_spaces = list(set(winning_spaces + these_spaces))

        # Check Diagonals "right-to-left"""
        this_board = self._diagonal_rows()
        these_spaces = self._check_rows(this_player, this_board)
        winning_spaces = list(set(winning_spaces + these_spaces))

        # Check Diagonals "left-to-right"
        this_board = self._diagonal_rows(reverse=True)
        these_spaces = self._check_rows(this_player, this_board)
        winning_spaces = list(set(winning_spaces + these_spaces))

        # Flag winning spaces
        if flag_winner:
            for space in winning_spaces:
                space.winner = True

        # player is winner if there are winning spaces for player
        if winning_spaces:
            return True
        else:
            return False

    def last_space_number(self):
        """
        Returns the board index of the last space of the board

        """
        return self.board[-1][-1].board_index

    def board_position_by_index(self, board_index):
        """
        Given a 1-based index, return the x, y coordinates on the game board

           1-Base Index

        4x3 Board: "6" == (1,1)

           1 | 2 | 3 | 4
          --- --- --- ---
           5 | 6 | 7 | 8
          --- --- --- ---
           9 | 10| 11| 12

        3x4 Board: "12" == (2,3)

           1 | 2 | 3
          --- --- ---
           4 | 5 | 6
          --- --- ---
           7 | 8 | 9
          --- --- ---
           10| 11| 12

        3x3 Board: "9" == (2,2)

           1 | 2 | 3
          --- --- ---
           4 | 5 | 6
          --- --- ---
           7 | 8 | 9

        """

        # Raise exception if not possible
        if board_index < 1 or board_index > (self.ROWS * self.COLS):
            msg = '"{}" is out of range for this board.'.format(board_index)
            raise BoardException(msg)

        for x, row in enumerate(self.board):
            for y, space in enumerate(row):
                if space.board_index == board_index:
                    return [x,y]

        msg = '"{}" was not found on this board.'.format(board_index)
        raise BoardException(msg)

    def _reset_last_move_flag(self):
        """
        reset last_move flag for every space on board

        """
        for row in self.board:
            for space in row:
                space.last_move = False

    def move_player(self, this_player, board_index):
        """
        Update the space to the value of the player and flag it so the space
        can be highlighted for the next players turn.

        If the targeted space is not a "blank" space then return False

        """
        x, y = self.board_position_by_index(board_index)
        # Check to see if the space is already occupied
        if self.board[x][y].player == self.P0:
            # set space to player
            self.board[x][y].player = this_player
            # flag the set space as a last move
            self._reset_last_move_flag()
            self.board[x][y].last_move = True
            return True
        else:
            return False

    def _place_player(self, this_player, board_index):
        """
        Same as move_player() except it is used by minimax to place players
        but not to change the last move flag

        """
        x, y = self.board_position_by_index(board_index)
        self.board[x][y].player = this_player

    def _un_place_player(self, board_index):
        """
        unplay a placed player set by minimax

        """
        x, y = self.board_position_by_index(board_index)
        self.board[x][y].player = self.P0

    def swap_players(self):
        """
        Swap the players as tracked by the board, not used by minimax

        """
        swap = self.next_player
        self.next_player = self.this_player
        self.this_player = swap

    def __str__(self):
        """
        Simple string representing which space the players are occupying

        """
        string = u''
        for rows in self.board:
            for space in rows:
                string += space.player
        return string