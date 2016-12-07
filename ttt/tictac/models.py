
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tictac.constants import SYMBOL_CHOICES


class Player(User):
    auto = models.BooleanField(_('is this a computer player?'),
        default=False)
    ai = models.CharField(_('What is the AI model used?'),
        default="boehner", max_length=64)

    def __init__(self, *args, **kwargs):
        """
        Rather than do a whole model for names, just tweak the one
        coming in a bit. Make up a random username. We don't care.
        """
        if (kwargs.get('name')):
            kwargs['first_name'] = kwargs['name']
            del kwargs['name']

        if not kwargs.get('username'):
            kwargs['username'] = uuid.uuid4().get_hex()

        super(Player, self).__init__(*args, **kwargs)

    def auto_move(self, board, number):
        """
        Perform ai-based moved using the various AIs that might be
        installed.
        """
        if (self.ai == 'boehner'):
            return self.ai_boehner(board, number)

    def ai_boehner(self, board, number):
        """
        Attempts to result in a tie by obstructing any possibility
        of a win. Wikipedia is a good source for strategy, here:

        http://en.wikipedia.org/wiki/Tic-tac-toe

            Win: If the player has two in a row, they can place a third
                to get three in a row.
            Block: If the opponent has two in a row, the player must play
                the third themself to block the opponent.
            Fork: Create an opportunity where the player has two threats
                to win (two non-blocked lines of 2).
            Blocking an opponent's fork:
                Option 1: The player should create two in a row to force the
                opponent into defending, as long as it doesn't result in them
                creating a fork. For example, if "X" has a corner, "O" has the
                center, and "X" has the opposite corner as well, "O" must not
                play a corner in order to win. (Playing a corner in this
                scenario creates a fork for "X" to win.)
                Option 2: If there is a configuration where the opponent
                can fork, the player should block that fork.
            Center: A player marks the center. (If it is the first move
                of the game, playing on a corner gives "O" more opportunities
                to make a mistake and may therefore be the better choice;
                however, it makes no difference between perfect players.)
            Opposite corner: If the opponent is in the corner, the player
                plays the opposite corner.
            Empty corner: The player plays in a corner square.
            Empty side: The player plays in a middle square on any of
                the 4 sides.

        """

        def test_str(string):
            """
            Check to see if a board will is winnish. Send back
            if it is at least a block situation, whether or not we
            would win if we played there, and where the hole is in the
            string.
            """

            block = False
            win = False
            pos = string.find(' ')

            # No move to be made here
            if pos < 0:
                return block, win, pos

            # _XX  XX_
            if string[1] != ' ' and (string[1] == string[2] or
                string[1] == string[0]):
                block = True
                win = string[1] == str(number)

            # X_X
            if string[0] != ' ' and (string[0] == string[2]):
                block = True
                win = string[0] == str(number)

            return block, win, pos


        state = board.state
        is_opening_move = state.find(str(number)) == -1

        if board.rows == board.columns and board.rows == 3:
            # only valid for 3x3

            col = None
            row = None

            # Make sure someone isn't about to win - either us or them
            # (but prefer us!) and play the hole if so
            #
            for counter in range(3):
                block, win, pos = test_str(state[counter*3:counter*3+3])
                if block:
                    row = counter
                    col = pos
                    if win:
                        return row, col
                block, win, pos = test_str(state[counter:9:3])
                if block:
                    row = pos
                    col = counter
                    if win:
                        return row, col

            # \
            diag = state[0:9:4]
            block, win, pos = test_str(diag)
            if block:
                row = pos
                col = pos
                if win:
                    return row, col

            # /
            diag = state[2:7:2]
            block, win, pos = test_str(diag)
            if block:
                row = pos
                col = 2-pos
                if win:
                    return row, col

            # We couldn't win, but if we can block we shou;d

            if row is not None:
                return row, col


            # OK, so we aren't #winning so let's do our next part
            # which is either make our first move (either center or
            # corner) or do our blocking, making sure we don't let
            # them fork.
            #
            if is_opening_move:
                order = (4, 0)
            else:
                order = (0, 2, 6, 8, 3, 5, 1, 7)
                # if their last move was into the corner, and they
                # have the opposite corner, play a side to keep them
                # from setting us up
                if board.last_move is not None and board.last_move in (0, 2, 6, 8):
                    if state[board.last_move] == state[8-board.last_move]:
                        order = (3, 5, 1, 7, ) + order
                    else:
                        # otherwise, play the opposite corner
                        order = (8-board.last_move, 0, 2, 6, 8, ) + order

            # Make the first one in the list that we can
            for pos in order:
                if state[pos] == ' ':
                    row = pos / 3
                    col = pos % 3
                    return row, col

        # We likely never get here, but since it's nice to have a default,
        # find first open slot and go there.
        pos = state.find(' ')
        if pos >= 0:
            row = pos / 3
            col = pos % 3

        return row, col


class Board(models.Model):
    """
    Represents a game board.
    """
    rows = models.IntegerField(default=3)
    columns = models.IntegerField(default=3)
    state = models.CharField(max_length=256)
    last_move = models.IntegerField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.last_move = None
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
            self.last_move = spot

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
                self.symbol = kwargs.get('symbol', '0123456789:;'[self.number])
            except IndexError:
                raise ValueError('Must specify symbol for player %d.' % (self.number, ))

        return None


class GameManager(models.Manager):
    def new_game(self, game_type='classic', players=[], auto_play=True):
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

                symbol = p.get('symbol')
                if symbol is not None:
                    del(p['symbol'])
                else:
                    symbol = SYMBOL_CHOICES[index]


                new_player, created = Player.objects.get_or_create(first_name=p.get('name'), defaults=p)
                new_player.auto = p.get('auto', False)
                new_player.save()

                player = GamePlayers(player=new_player, game=game,
                    number=index, symbol=symbol)
                player.save()
                index = index + 1

            if auto_play:
                game.play_auto_turns()

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

        def _test_win(str):
            return str[0] != ' ' and str.count(str[0]) == 3

        # we assume classic boards are 3x3
        if self.board.columns != 3 or self.board.rows != 3:
            raise ValueError('Cannot determine classic winner for a non-3x3 game.')

        state = self.board.state
        for counter in range(3):
            # -
            if _test_win(state[counter*3:counter*3+3]):
                return True
            # |
            if _test_win(state[counter:9:3]):
                return True

        # \
        if _test_win(state[0:9:4]):
           return True

        # /
        if _test_win(state[2:7:2]):
            return True

        return False

    def next_gameplayer(self):
        """
        The game player is determined by the turn modulo the number of
        players.
        """
        player_number = self.turn_counter % self.players.count()
        player = GamePlayers.objects.get(game=self, number=player_number)
        return player

    def play_auto_turns(self):
        """
        As long as we have an AI player, let it take its turn. When we
        hit a carbon unit, relenquish.
        """
        game_player = self.next_gameplayer()
        new_state = self.board.state

        while game_player.player.auto == True and not self.game_over:

            row, column = game_player.player.auto_move(self.board, game_player.number)

            new_state = self.board.mark_play(row, column, game_player.number)

            winning = self.has_winning_board() #winning
            if winning or self.has_full_board():
                self.game_over = True
                if winning:
                    self.winner = game_player.player
            else:
                self.turn_counter = self.turn_counter + 1

            game_player = self.next_gameplayer()

        self.save()

        return new_state

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

        # play any automatic turns after the ugly bags of mostly water
        # get to do their (inferior) thing.
        return self.play_auto_turns()

