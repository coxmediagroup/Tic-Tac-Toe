from collections import Counter
from django.core.urlresolvers import reverse
from django.db import models


class Game(models.Model):
    """
    This defines the board state (and metadata) for a tic-tac-toe game.

    The board is modeled a 9 character string:
        'X' or 'O' means the space is played.
        ' ' (space) means the space is empty.

    We also keep track of the time the game was created and last updated,
    just in case we want to add "recent games" or a game list of some form.

    In addition, it includes the player types. Since this is somewhat
    insulated from the view layer of the application, we should be
    generic about the player types and not make assumptions about
    what the UI can support -- for instance, we should be able
    to support two human players, or potentially two computer players
    (although the latter would be quite dull).

    We also need to support different computer player types. Each
    player field (player_x or player_o) is a string that specifies
    either "human" or a player object type.

    Note right now we aren't robust against degenerate cases --
    we don't prevent you from saving board states that are impossible
    given the game rules.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    board = models.CharField(max_length=9, default=" " * 9)

    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)


    def __unicode__(self):
        return '{0} vs {1}, state="{2}"'.format(self.player_x, self.player_o, self.board)

    def get_absolute_url(self):
        return reverse('game:detail', kwargs={'pk': self.pk})

    @property
    def next_player(self):
        """
        Returns 'X' if the next play is player X, otherwise 'O'.
        This is easy to calculate based on how many plays have taken place:
        if X has played more than O, it's O's turn; otherwise, X plays.
        """
        # Counter is a useful class that counts objects.
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'

    WINNING = [
        [0, 1, 2],  # Across top
        [3, 4, 5],  # Across middle
        [6, 7, 8],  # Across bottom
        [0, 3, 6],  # Down left
        [1, 4, 7],  # Down middle
        [2, 5, 8],  # Down right
        [0, 4, 8],  # Diagonal ltr
        [2, 4, 6],  # Diagonal rtl
    ]

    @property
    def is_game_over(self):
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' ' (space)
        If the game isn't over, it returns None.

        The test is to simple check for each combination of winnable
        states --- across, down, and diagonals.
        If none of the winning states is reached and there are
        no empty squares, the game is declared a stalemate.
        """
        the_board = list(self.board)
        for wins in self.WINNING:
            # Create a tuple
            w = (the_board[wins[0]], the_board[wins[1]], the_board[wins[2]])
            if w == ('X', 'X', 'X'):
                return 'X'
            if w == ('O', 'O', 'O'):
                return 'O'
        # Check for stalemate
        if ' ' in the_board:
            return None
        return ' '

    def play(self, index):
        """
        Plays a square specified by ``index``.
        The player to play is implied by the board state.

        If the play is invalid, it raises a ValueError.
        """
        if index < 0 or index >= 9:
            raise IndexError("Invalid board index")

        if self.board[index] != ' ':
            raise ValueError("Square already played")

        # One downside of storing the board state as a string
        # is that you can't mutate it in place.
        board = list(self.board)
        board[index] = self.next_player
        self.board = u''.join(board)

    def play_auto(self):
        """Plays for any artificial/computers players.
        Returns when the computer players have played or the game is over."""
        from .players import get_player

        while not self.is_game_over:
            next = self.next_player
            player = self.player_x if next == 'X' else self.player_o
            if player == 'human':
                return

            player_obj = get_player(player)
            self.play(player_obj.play(self))
