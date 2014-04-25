
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

    def is_valid_move(self, row, column):
        # is that on the board
        if row < 0 or row >= self.rows or column < 0 or column >= self.columns:
            return False
        return True

    def can_play(self, row, column):
        if not self.is_valid_move(row, column):
            raise Exception('Space %d, %d is not on this %sx%x board.' % (
                row, column, self.rows, self.columns, ))

        spot = row*self.columns + column
        try:
            return self.state[spot] == ' '
        except:
            return False

    def mark_play(self, row, column, number=None):
        if not self.is_valid_move(row, column):
            raise Exception('Space %d, %d is not on this %sx%x board.' % (
                row, column, self.rows, self.columns, ))

        if number is None:
            raise Exception('Who is playing this?')

        if self.can_play(row, column):
            spot = row*self.columns + column

            self.state = "%s%1d%s" % (self.state[0:spot], number, self.state[spot+1:], )
            self.save()
            return self.state

        raise Exception('Can\'t play that spot.')


class GamePlayers(models.Model):
    """
    Thru class for game-player matches.
    """
    player = models.ForeignKey('Player',
        verbose_name=_('player'), help_text='dont hate')
    game = models.ForeignKey('Game',
        verbose_name=_('game'), help_text='hate')
    number = models.IntegerField()
    symbol = models.CharField(max_length=8)

    def __init__(self, *args, **kwargs):

        super(GamePlayers, self).__init__(*args, **kwargs)

        if not self.player or not self.game or self.number < 0:
            raise ValueError('Not enough info to add player to game.')

        if not self.symbol:
            try:
                self.symbol = kwargs.get('symbol', 'XO+IS'[self.number])
            except IndexError:
                raise ValueError('Must specify symbol for player %d.' % (self.number, ))

        return None


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

            index = 0
            for p in players:
                new_player, created = Player.objects.get_or_create(first_name=p.get('name'), defaults=p)
                player = GamePlayers(player=new_player, game=game, number=index)
                player.save()
                index = index + 1

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
        related_name='players',
        through='GamePlayers')

    turn_counter = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)
    last_play = models.DateTimeField(auto_now=True)

    game_over = models.BooleanField(default=False)
    winner = models.ForeignKey('Player', related_name='games_won',
        blank=True, null=True, )

    objects = GameManager()

    def has_full_board(self):
        return self.board.state.find(' ') < 0

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

    def next_gameplayer(self):
        player_number = self.turn_counter % self.players.count()
        player = GamePlayers.objects.get(game=self, number=player_number)
        return player

    def play_turn(self, player, position=None, row=None, column=None):

        if type(player) == int:
            player = GamePlayers.objects.get(game=self, number=player)

        if position is not None:
            row = position / self.board.columns
            column = position % self.board.columns

        game_player = self.next_gameplayer()
        if game_player != player:
            raise Exception('Not your turn, %s.' % (player.player.first_name))

        if not self.board.can_play(row, column):
            raise Exception('That space is already taken.')

        new_state = self.board.mark_play(row, column, game_player.number)

        # Winner?

        winning = self.has_winning_board() #winning
        if winning or self.has_full_board():
            self.game_over = True
            if winning:
                self.winner = game_player.player
        else:
            self.turn_counter = self.turn_counter + 1

        self.save()

        return new_state


