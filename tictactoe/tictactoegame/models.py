from django.db import models


class Game(models.Model):
	board = models.CharField(max_length=9)
    poll = models.ForeignKey(Player)

class Player(models.Model):
    name = models.CharField(max_length=200)