
import uuid
from django.contrib.auth.models import User

from django.db import models

from django.utils.translation import ugettext_lazy as _

class Player(User):
    auto = models.BooleanField(_('is this a computer player?'),
        default=False)

    def __init__(self, *args, **kwargs):
        if (kwargs.get('name')):
            kwargs['first_name'] = kwargs['name']
            del kwargs['name']

        if not kwargs.get('username'):
            kwargs['username'] = uuid.uuid4().get_hex()

        super(Player, self).__init__(*args, **kwargs)


class Board(models.Model):
    """
    Represents a game board.
    """
    rows = models.IntegerField(default=3)
    columns = models.IntegerField(default=3)
    state = models.CharField(max_length=256)

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        if not self.state:
            self.state = ' '*(self.rows*self.columns)
        self.save()

    def __repr__(self):
        lines = [
          ' ' + ' | '.join(['%s' % (self.state[row*self.columns+col]) for col in range(self.columns)])
          for row in range(self.rows) ]
        sep = '\n==' + '=+==' * (self.columns - 1) + '=\n'
        return '\n' + sep.join(lines)

class GameManager(models.Manager):
    def new_game(self, game_type='classic', players=[]):
        """
        Creates a new game.

        Currently only supports two-player classic games.
        """
        if game_type == 'classic' and len(players) <= 2 and len(players) > 0:

            game = Game(game_type=game_type)
            game.board = Board(rows=3, columns=3)
            game.save()

            for p in players:
                new_player, created = Player.objects.get_or_create(first_name=p.get('name'), defaults=p)
                game.players.add(new_player)

            game.save()
            return game

        raise ValueError('Can only play "classic" tic-tac-to right now.')


class Game(models.Model):
    """
    Represents a game, which is essentially a combination
    of state, a board, and players.
    """
    game_type = models.CharField(_('type of game'), max_length=32,
        default='classic')
    board = models.ForeignKey('Board',
        verbose_name=_('board'), )
    players = models.ManyToManyField('Player',
        verbose_name=_('players'),
        related_name='players')

    turn_counter = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)
    last_play = models.DateTimeField(auto_now=True)

    game_over = models.BooleanField(default=False)
    winner = models.ForeignKey('Player', related_name='games_won',
        blank=True, null=True, )

    objects = GameManager()

    def has_winning_board(self, *args, **kwargs):
        if self.game_type == 'classic':
            return self._classic_has_winning_board(*args, **kwargs)

        return False

    def _classic_has_winning_board(self, debug=False):

        # we assume classic boards are 3x3
        if self.board.columns != 3 or self.board.rows != 3:
            raise ValueError('Cannot determine classic winner for a non-3x3 game.')

        strs = [''] * 8

        for idx in range(0, 3):
            strs[idx] = self.board.state[3*idx:3*idx+3]
            strs[3] = strs[3] + self.board.state[3*idx]
            strs[4] = strs[4] + self.board.state[3*idx+1]
            strs[5] = strs[5] + self.board.state[3*idx+2]
            strs[6] = strs[6] + self.board.state[3*idx+idx]
            strs[7] = strs[7] + self.board.state[3*idx+2-idx]

        # if we're debugging, we can return the strs to check and
        # whether it is a win
        #
        if debug:
            return [(check, check[0] != ' ' and check.count(check[0]) == 3) for check in strs]

        for check in strs:
            if check[0] != ' ' and check.count(check[0]) == 3:
                return True

        return False



