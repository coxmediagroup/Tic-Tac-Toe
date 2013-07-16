"""
Class to represent a Tic-Tac-Toe game board.
"""
from errors import TicTacToeError
import errorcodes


class Board(object):
    """
    Class to represent a Tic-Tac-Toe game board.
    """

    # All of the combinations of moves (in terms of absolute position) that will determine the winner.
    WIN_MOVES = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]

    def __init__(self):
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
            error_fmt = "Position already selected: {0} ({1})"
            prev_selection = 'X' if absolute_pos in self.x_positions else 'O'
            error_msg = error_fmt.format(absolute_pos, prev_selection)
            raise TicTacToeError(error_msg, errorcodes.POSITION_ALREADY_SELECTED)
        set_to_add = self.x_positions if mark in ('X', 'x') else self.o_positions
        set_to_add.add(absolute_pos)

    def _find_best_move(self, mark):
        """
        Try and find the 'best' move for the given C{mark}, which should either be 'X' or 'O'.

        @param mark: The mark to compute the best move for ('X' or 'O')
        @type mark: str
        @return: The absolute position of the best move for C{mark} (0-8).
        @rtype: int
        """
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
