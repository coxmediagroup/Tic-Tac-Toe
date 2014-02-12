from django.db import models

PLAYER_X = 1
PLAYER_NONE = 0
PLAYER_O = -1


class Game(models.Model):
    is_user_x = models.BooleanField(default=True)
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, default=None)

    @classmethod
    def create_new(cls, is_user_x=True):
        game = Game()
        game.is_user_x = is_user_x
        game.save()

        board = Board()
        board.game = game
        board.save()

        assert game._board == board

        return game


class Board(models.Model):
    game = models.OneToOneField(Game, related_name='_board')
    upper_left = models.SmallIntegerField(default=0)
    upper_center = models.SmallIntegerField(default=0)
    upper_right = models.SmallIntegerField(default=0)
    center_left = models.SmallIntegerField(default=0)
    center = models.SmallIntegerField(default=0)
    center_right = models.SmallIntegerField(default=0)
    lower_left = models.SmallIntegerField(default=0)
    lower_center = models.SmallIntegerField(default=0)
    lower_right = models.SmallIntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)
