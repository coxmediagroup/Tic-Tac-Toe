"""
Class to represent a Tic-Tac-Toe game board.
"""
from errors import TicTacToeError
import errorcodes
import random


class Board(object):
    """
    Class to represent a Tic-Tac-Toe game board.
    """

    # All of the combinations of moves (in terms of absolute position) that will determine the winner.
    WIN_MOVES = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    # The corners of the game board, in counterclockwise order.
    CORNERS = [0, 6, 8, 2]

    def __init__(self):
        """
        Create a new Tic-Tac-Toe game board by initializing the sets of X and O positions.
        """
        self.x_positions = set()
        self.o_positions = set()

    def add_mark(self, absolute_pos, mark):
        """
        Add the given mark to this Tic-Tac-Toe board. The mark should be an X or an O.

        @param absolute_pos: The absolute position (0-8) to mark on the board
        @type absolute_pos: int
        @param mark: The letter to mark on the board
        @type mark: str
        """
        if absolute_pos in self.x_positions or absolute_pos in self.o_positions:
            error_fmt = "Position {0} is already selected by {1}"
            prev_selection = 'X' if absolute_pos in self.x_positions else 'O'
            error_msg = error_fmt.format(absolute_pos, prev_selection)
            raise TicTacToeError(error_msg, errorcodes.POSITION_ALREADY_SELECTED)
        set_to_add = self.x_positions if mark in ('X', 'x') else self.o_positions
        set_to_add.add(absolute_pos)

    def find_next_move(self, mark):
        """
        Given the mark ('X' or 'O') of the desired side, find the best next move that side can make.

        @param mark: The mark of the desired side ('X' or 'O')
        @type mark: str
        @return: The absolute position (0-8) of the best possible move for the given mark
        @rtype: int
        """
        # Determine my positions, the other set of positions, and who is/was first.
        my_positions = self.x_positions if mark in ('X', 'x') else self.o_positions
        other_positions = self.o_positions if mark in ('X', 'x') else self.x_positions
        i_was_first = len(other_positions) <= len(my_positions)

        # If I can make a winning move, return its position.
        my_win_moves = self.get_winning_moves(my_positions, other_positions)
        if my_win_moves != []:
            return my_win_moves[0]

        # If I can block my opponent from winning, return the first such position that will do so.
        # (there should be at most 1 such position if/when the computer calls this)
        my_block_moves = self.get_winning_moves(other_positions, my_positions)
        if my_block_moves != []:
            return my_block_moves[0]

        # If my opponent went first, play the middle square if it hasn't already been played.
        if not i_was_first and 4 not in my_positions and 4 not in other_positions:
            return 4

        # If I'm first and no one has taken a turn, pick one of the corner squares.
        if i_was_first and len(my_positions) == 0 and len(other_positions) == 0:
            return random.choice(self.CORNERS)

        # If I'm first and this is my second turn, determine if my opponent picked an adjacent corner.
        # If so, pick the opposite corner. Otherwise, pick any of the adjacent corners.
        if i_was_first and len(other_positions) == 1 and list(my_positions)[0] in self.CORNERS:
            my_index = self.CORNERS.index(list(my_positions)[0])
            adj_corners = (self.CORNERS[(my_index - 1) % 4], self.CORNERS[(my_index + 1) % 4])
            opposite_corner = self.CORNERS[(my_index + 2) % 4]
            other_pos = list(other_positions)[0]
            if other_pos in adj_corners:
                return opposite_corner
            else:
                return random.choice(adj_corners)

        # If none of the above are true, try brute-forcing the next best move.
        return self._find_best_move(mark)

    def _find_best_move(self, mark):
        """
        Try and find the 'best' move for the given C{mark}, which should either be 'X' or 'O'.

        @param mark: The mark to compute the best move for ('X' or 'O')
        @type mark: str
        @return: The absolute position of the best move for C{mark} (0-8).
        @rtype: int
        """
        # Create 2 temporary functions to get our positions or those of our opponent, depending on the mark
        # we were passed.
        if mark in ('X', 'x'):
            get_my_pos = lambda board: board.x_positions
            get_other_pos = lambda board: board.o_positions
        else:
            get_my_pos = lambda board: board.o_positions
            get_other_pos = lambda board: board.x_positions

        my_positions = get_my_pos(self)
        other_positions = get_other_pos(self)
        unplayed_positions = set(xrange(0, 9)) - my_positions - other_positions

        if len(unplayed_positions) == 0:
            error_msg = "The board has already been filled!"
            raise TicTacToeError(error_msg, errorcodes.NO_POSITIONS_AVAILABLE)

        # Assemble a dictionary whose keys are the number of moves resulting in a win and whose values are
        # a list of corresponding unplayed positions.
        move_dict = {}
        for position in unplayed_positions:
            possible_board = Board()
            for x_pos in self.x_positions:
                possible_board.add_mark(x_pos, 'X')
            for o_pos in self.o_positions:
                possible_board.add_mark(o_pos, 'O')
            possible_board.add_mark(position, mark)
            my_new_pos = get_my_pos(possible_board)
            other_new_pos = get_other_pos(possible_board)
            future_moves = possible_board.get_winning_moves(my_new_pos, other_new_pos)
            move_dict.setdefault(len(future_moves), []).append(position)
        best_moves = max(move_dict)
        return move_dict[best_moves][0]

    def get_winner(self):
        """
        Get the winner of the game represented by this L{Board}, if there is one.

        @return: The winner
        @rtype: str
        """
        for wm in self.WIN_MOVES:
            if wm - self.x_positions == set():
                return "X"
            if wm - self.o_positions == set():
                return "O"

    @property
    def is_playable(self):
        """
        Return True if the current board is playable (i.e. there is no winner and there are unplayed spaces).

        @return: True if the current board is playable, otherwise False
        @rtype: bool
        """
        if self.get_winner() in ("X", "O"):
            return False
        return bool(set(xrange(0, 9)) - self.x_positions - self.o_positions)

    @classmethod
    def get_winning_moves(cls, my_positions, other_positions):
        """
        Get a list of moves that can be made by the target player (whose positions are given by
        C{my_positions}) in order to win the current game.

        @param my_positions: The set of positions for the player whose winning moves are being found
        @type my_positions: set
        @param other_positions: The set of positions for the player's opponent
        @type other_positions: set
        @return: A list of possible moves the target player can make to win the game
        @rtype: list [int]
        """
        possible_moves = []
        for wm in cls.WIN_MOVES:
            missing = wm - my_positions
            if len(missing) != 1:
                continue
            my_win = missing.pop()
            if my_win in other_positions:
                continue
            possible_moves.append(my_win)
        return possible_moves

    def get_mark(self, absolute_pos):
        """
        Return an 'X' or an 'O' (surrounded by spaces) or the absolute position (surrounded by parentheses)
        depending on whether or not C{absolute_pos} is occupied, and/or who is occupying it.

        @param absolute_pos: The absolute position (0-8) whose mark we want to retrieve
        @type absolute_pos: int
        @return: The mark associated with C{absolute_pos}
        @rtype: str
        """
        if absolute_pos in self.x_positions:
            return " X "
        elif absolute_pos in self.o_positions:
            return " O "
        return "({0})".format(absolute_pos)

    def print_board(self):
        """
        Print the Tic-Tac-Toe board to the console in standard format.
        """
        print "     |     |     "
        print " {0} | {1} | {2} ".format(self.get_mark(0), self.get_mark(1), self.get_mark(2))
        print "     |     |     "
        print "-----|-----|-----"
        print "     |     |     "
        print " {0} | {1} | {2} ".format(self.get_mark(3), self.get_mark(4), self.get_mark(5))
        print "     |     |     "
        print "-----|-----|-----"
        print "     |     |     "
        print " {0} | {1} | {2} ".format(self.get_mark(6), self.get_mark(7), self.get_mark(8))
        print "     |     |     "
        if self.is_playable:
            return
        winner = self.get_winner()
        print "\nWinner: {0}".format(winner or "KITTY")
