from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    session = models.CharField(max_length=200)


class Game(models.Model):
    board = models.CharField(max_length=9)
    is_active=models.BooleanField()
    player = models.ForeignKey(Player)

