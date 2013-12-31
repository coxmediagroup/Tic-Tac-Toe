from django.db import models


class AllGames(models.Model):
    total_games = models.IntegerField()
    computer_wins = models.IntegerField()

class SingleGame(models.Model):
    state = models.CharField(max_length = 50)
    player_piece = models.CharField(max_length = 1)


