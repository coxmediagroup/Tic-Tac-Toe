from django.db import models


class AllGames(models.Model):
    total_games = models.IntegerField()
    computer_wins = models.IntegerField()

class SingleGame(models.Model):
    state = models.CharField(max_length = 50)
    player_piece = models.CharField(max_length = 1)
    
    def move_added(self, spot):
        self.make_move(spot, 'P')
        computer_move = self.make_computer_move(1, 'C')
        return computer_move

    def make_move(self, spot, piece):
        if len(self.state) > 0:
            self.state += ',' + str(spot) + piece
        else:
            self.state = str(spot) + piece
        self.save()
        return

    def make_computer_move(self, spot, player):
        return spot

        



