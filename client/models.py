from django.db import models

class Game(models.Model):

    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % (self.name)

class Move(models.Model):

    board = models.CharField(max_length=25)
    game = models.ForeignKey(Game)
    x_position = models.IntegerField()
    y_position = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%d: %s (%d,%d)" % (self.pk, self.game.name, self.x_position, self.y_position)