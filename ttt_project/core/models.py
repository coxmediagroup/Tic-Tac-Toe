from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id


class Move(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(User)
    computer = models.BooleanField(default=False)
    space = models.IntegerField()

    def __unicode__(self):
        return "Move for game %s" % self.game

