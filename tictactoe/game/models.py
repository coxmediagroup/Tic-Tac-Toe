from django.db import models
from random import choice


class AllGames(models.Model):
    total_games = models.IntegerField()
    computer_wins = models.IntegerField()

class SingleGame(models.Model):
    state = models.CharField(max_length = 50)
    player_piece = models.CharField(max_length = 1)
    
    def move_added(self, spot):
        self.make_move(spot, 'P')
        computer_move = self.make_computer_move()
        self.make_move(computer_move, 'C')
        return computer_move

    def make_move(self, spot, piece):
        if len(self.state) > 0:
            self.state += ',' + str(spot) + piece
        else:
            self.state = str(spot) + piece
        self.save()
        return

    def make_computer_move(self):
        return choice(self.get_unused_squares(self.state))
    
    def get_unused_squares(self, state):
        unused_squares = []
        for num in range(0,9):
            if state.find(str(num)) == -1:
                unused_squares.append(num)
        return unused_squares


        



