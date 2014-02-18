__author__ = 'henryadam'

import random

class PositionAlreadyTakenError(Exception):
    pass

class Board(object):
    """a tic tac toe matrix"""
    wins = ((0,1,2), # rows
            (3,4,5),
            (6,7,8),
            (0,3,6), # columns
            (1,4,7),
            (2,5,8),
            (0,4,8), # diagonals
            (2,4,6))

    def __init__(self, *args, **kwargs):
        """
            The board is the passed in board or a blank board since this AI always wins, we will always render
            an initialized board where the computer takes the middle
        """
        self.the_board = kwargs.get('the_board',[None, None, None, None, None, None, None, None, None])

    def select_position(self, position, player):
        """Sets a position on the board as owned by a player"""

        if self.the_board[position] is not None:
            raise PositionAlreadyTakenError()

        self.the_board[position] = player.board_value

    def check_for_win(self, player):
        """Check the board to see if the player has won"""
        winner = False
        for group in Board.wins:
            if self.the_board[group[0]] == player.board_value \
                    and self.the_board[group[1]] == player.board_value \
                    and self.the_board[group[2]] == player.board_value:
                winner = True
                break

        return winner

    def draw(self):
        """
            This function will draw a bootstrap html table based on a sequence received in the argument board
            so that a board [0,1,2,3,4,5,6,7,8]
        """
        for index,value in enumerate(self.the_board):
            if value == None:
                self.the_board[index] = str('')

        draw_this = """<div  class="row-fluid">
                <div id="cell_0" class="offset1 span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_1" class="span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_2" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>
            <div class="row-fluid">
                <div id="cell_3" class="offset1 span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_4" class="span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_5" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>
            <div class="row-fluid">
                <div id="cell_6" class="offset1 span3 well">
                   <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_7" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
                <div id="cell_8" class="span3 well">
                    <h1 class="text-center">%s</h1>
                </div>
            </div>""" % (self.the_board[0] ,self.the_board[1],self.the_board[2],self.the_board[3],self.the_board[4],self.the_board[5],self.the_board[6],self.the_board[7],self.the_board[8])
        return(draw_this)

class Player(object):
    """A tic tact toe player"""

    def __init__(self, board_value, *args, **kwargs):
        """
        board_value should be a single character to display such as X or O.
        """

        # the value which will represent the player behind the scenes
        self.board_value = board_value
        self.turn_count = 0

class AIPlayer(Player):
    """I am the AI player for this game"""
    # These are the positions to target in order
    # Each list index aligns with the corresponding board position
    STRATEGIES = [(4, 8, 2),
                  (4, 8, 6, 2, 0),
                  (4, 6, 0),
                  (4, 0, 2, 6, 8),
                  None, # should not happen, we ALWAYS get this first
                  (4, 0, 2, 6, 8),
                  (4, 2, 8),
                  (4, 0, 2, 6, 8),
                  (4, 0, 6)]

    def __init__(self, board_value, *args, **kwargs):
        super(AIPlayer, self).__init__(board_value, *args, **kwargs)
        self.strategy = None

    def look_for_win(self, board, player=None):
        """Find a space which allows a win for the given player"""
        win_spot = None
        if player is None:
            player = self

        for group in board.wins:
            # creates a list of just the elements of the board which are
            # part of a specific win group and and not already owned by the player
            # and creates a list of tuples of the element and its value.
            not_mine = [(i, val) for i, val in enumerate(board.the_board)
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

        open_positions = [i for i, value in enumerate(board.the_board) if value is None]

        # default no priority position then see if there's a position open
        # which fits the chosen strategy
        selected_position = open_positions[0]

        for position in self.strategy:
            if position in open_positions:
                selected_position = position
                break

        return selected_position

    def take_turn(self, board, other_player):
        """Implement the logic for a single turn of the AI player"""

        # Always pick the middle box on the first round
        position = None


        # On the second turn, after the human player has picked
        # their first spot so we can determine our strategy
        assert other_player.board_value in board.the_board
        player2_position = board.the_board.index(other_player.board_value)
        self.strategy = AIPlayer.STRATEGIES[player2_position]

        if position is None:
            position = self.look_for_win(board)

        if position is None:
            position = self.look_for_win(board, other_player)

        if position is None:
            position = self.pick_open_position(board)


        return position