from django.db import models

# Create your models here.

class Entity(models.Model):
    is_ai = models.BooleanField(default=False)

class Location(models.Model):
    column = models.IntegerField()
    row = models.ForeignKey(Row)
    occupier = models.ForeignKey(Entity)

class Row(models.Model):
    board = models.ForeignKey(Board)
    row = models.IntegerField()

class Board(model.Model):
    game = models.ForeignKey(Game)

class Game(model.Model):
    board = models.ForeignKey(Board)
    current_player = models.ForeignKey(Entity)
