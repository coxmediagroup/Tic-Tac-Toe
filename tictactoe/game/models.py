import logging
from django.db import models
from picklefield.fields import PickledObjectField

class TicTacToeModel(models.Model):
    gameID = models.AutoField(primary_key=True)
    sessionID = models.CharField(max_length=255, help_text="Used to prevent the user from affecting other games by form editing.")
    playerCharacter = models.CharField(max_length=1, help_text="Determines if they are X or O.")
    boardSize = models.IntegerField()
    gameBoard = PickledObjectField()