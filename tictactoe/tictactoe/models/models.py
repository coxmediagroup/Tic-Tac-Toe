from django.db import models

class Game(models.Model):
    pass

class Play(models.Model):
    game = models.ForeignKey(Game)
    pass