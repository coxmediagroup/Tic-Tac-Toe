from django.db import models


class Game(models.Model):
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.id


class Move(models.Model):
    game = models.ForeignKey(Game)
    player_move = models.BooleanField(default=True)
    space = models.IntegerField()

    def __unicode__(self):
        return "Move for game %s in space %s" % (self.game, self.space)

