
import random
from ttt.board import board


class AbstractPlayer:
    """
    Base representation of a player.  Should not be used directly, but as part
    of TextPlayer(AbstractPlayer), GUIPlayer(AbstractPlayer), etc.

    Also gives us a good place to contain the Computer Player logic
    """
    def __init__(self, marker):
        self.marker = marker

    def get_square(self, current_board, message):
        raise NotImplemented


class ComputerPlayer(AbstractPlayer):

    def get_square(self, current_board, message):
        """
        Very naive implementation.  Will be around just long enough for
          testing.
        """
        if current_board.is_empty():
            return 4

        i = None
        while True:
            i = random.randint(0, current_board.size-1)
            if current_board.square_free(i):
                return i
