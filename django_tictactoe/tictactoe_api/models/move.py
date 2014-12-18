from django.db import models

class Move(models.Model):
  """Database model for tic-tac-toe moves.
     Each game is a sequence of moves in order. The player
     and position played is recorded for each player's move"""
  session_id = models.CharField(max_length=36)
  insert_id =  models.AutoField(primary_key=True)
  player =     models.CharField(max_length=1)
  position =   models.IntegerField()

