"""
A simple tic tac toe game where the computer always wins or at least ties.
"""


class Board(object):
    """A tic tac toe board"""

    wins = ((0,1,2), # rows
            (3,4,5),
            (6,7,8),
            (0,3,6), # columns
            (1,4,7),
            (2,5,8),
            (0,4,8), # diagonals
            (2,4,6))

    def __init__(self, *args, **kwargs):
        self.tttboard = [None, None, None,
                         None, None, None,
                         None, None, None]


class Player(object):
    """A tic tact toe player"""

    def __init__(self, board_value, *args, **kwargs):
        """
        board_value should be a single character to display such as X or O.
        """

        self.board_value = board_value  # the value which will represent the player behind the scenes

class AIPlayer(Player):
    """An AI tic tac toe player"""

    # High priority board positions in order that they should be selected
    # if the position is open and there are no higher priorities such as
    # a winning opening or blocking a win.
    # This is the middle and then the 4 corners, the positions with the most
    # opportunity for leading to a win.
    POSITION_PRIORITY = (4, 0, 2, 6, 8)

    def look_for_win(self, board, player=None):
        """Find a space which allows a win for the given player"""

        win_spot = None
        if player is None:
            player = self

        for group in board.wins:
            # creates a list of just the elements of the board which are
            # part of a specific win group and and not already owned by the player
            # and creates a list of tuples of the element and its value.
            not_mine = [(i, val) for i, val in enumerate(board.tttboard)
                        if i in group
                        and val != player.board_value]

            # If there's only one not owned by the ai player and not owned by
            # the other player then select it and we've won
            if len(not_mine) == 1 and not_mine[0][1] is None:
                # Maybe this should return the selection rather than
                # modifying the board in here.  Decide later.
                win_spot=not_mine[0][0]
                break

        return win_spot

    def pick_open_position(self, board):
        """
        Select any open spot on the board.

        This is a fallback to be used when there are no wins or win blockers.
        """

        open_positions = [i for i, value in enumerate(board.tttboard) if value is None]

        # default no priority position
        selected_position = open_positions[0]

        for position in AIPlayer.POSITION_PRIORITY:
            if position in open_positions:
                selected_position = position
                break


        return selected_position

