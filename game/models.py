from django.db import models

class Game(models.Model):
    is_user_x    = models.BooleanField(default=True)
    started      = models.DateTimeField(auto_now_add=True)
    ended        = models.DateTimeField(null=True, default=None)

class Board(models.Model):
    game         = models.OneToOneField(Game)
    upper_left   = models.SmallIntegerField(default=0)
    upper_center = models.SmallIntegerField(default=0)
    upper_right  = models.SmallIntegerField(default=0)
    center_left  = models.SmallIntegerField(default=0)
    center       = models.SmallIntegerField(default=0)
    center_right = models.SmallIntegerField(default=0)
    lower_left   = models.SmallIntegerField(default=0)
    lower_center = models.SmallIntegerField(default=0)
    lower_right  = models.SmallIntegerField(default=0)
    last_played  = models.DateTimeField(auto_now=True)

