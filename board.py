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
        Return an 'X', an 'O', or a blank space, depending on whether or not C{absolute_pos} is occupied, and
        who is occupying it.

        @param absolute_pos: The absolute position (0-8) whose mark we want to retrieve
        @type absolute_pos: int
        @return: The mark associated with C{absolute_pos}
        @rtype: str
        """
        if absolute_pos in self.x_positions:
            return "X"
        elif absolute_pos in self.o_positions:
            return "O"
        return " "

    def print_board(self):
        """
        Print the Tic-Tac-Toe board to the console in standard format.
        """
        print "   |   |   "
        print " {0} | {1} | {2} ".format(self.get_mark(0), self.get_mark(1), self.get_mark(2))
        print "   |   |   "
        print "---|---|---"
        print "   |   |   "
        print " {0} | {1} | {2} ".format(self.get_mark(3), self.get_mark(4), self.get_mark(5))
        print "   |   |   "
        print "---|---|---"
        print "   |   |   "
        print " {0} | {1} | {2} ".format(self.get_mark(6), self.get_mark(7), self.get_mark(8))
        print "   |   |   "

