__author__ = 'marc'

class PositionAlreadyTakenError(Exception):
    pass

class Board(object):
    """A tic tac toe board"""


    def __init__(self, *args, **kwargs):
        self.tttboard = [None, None, None,
                         None, None, None,
                         None, None, None]

    def select_position(self, position, player):
        """Sets a position on the board as owned by a player"""

        if self.tttboard[position] is not None:
            raise PositionAlreadyTakenError({"message":"That position is already taken"})

        self.tttboard[position] = player.board_value