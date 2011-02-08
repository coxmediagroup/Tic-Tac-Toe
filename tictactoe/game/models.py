from django.db import models
from game.fields import TicTacToeBoardField
from itertools import chain

class Game(models.Model):
    """A tic-tac-toe game."""
    board_state = TicTacToeBoardField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_game_over(self):
        """
        Returns true if the game is over.

        "Game Over" could mean that someone has won or there is a tie.  Check
        ``get_winner`` to find out.
        """
        # Flatten the two-dimensional array to simplify checking for a tie.
        flattened_board = chain.from_iterable(self.board_state)
        return (self.get_winner() or None not in flattened_board)

    def get_winner(self):
        """
        Returns the winner.  If there is no winner, either due to a draw or
        incomplete game, None will be returned.
        """
        bs = self.board_state

        for i in xrange(0, 3):
            # Check rows.
            if bs[i][0] == bs[i][1] == bs[i][2] and bs[i][0] is not None:
                return bs[i][0]

            # Check columns.
            if bs[0][i] == bs[1][i] == bs[2][i] and bs[0][i] is not None:
                return bs[0][i]

        # Check diagonals.
        if ((bs[0][0] == bs[1][1] == bs[2][2]) or (bs[0][2] == bs[1][1] == bs[2][0])) \
            and bs[1][1] is not None:
                return bs[1][1]

        return None
