from django.db import models

class Game(models.Model):
    player = models.CharField(max_length=1)
    computer = models.CharField(max_length=1)
    board = models.CharField(max_length=9)
