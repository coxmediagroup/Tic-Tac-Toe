from django.db import models
from random import choice


class AllGames(models.Model):
    total_games = models.IntegerField()
    computer_wins = models.IntegerField()

class SingleGame(models.Model):
    state = models.CharField(max_length = 50)
    player_piece = models.CharField(max_length = 1)
    
    WINNING_COMBINATIONS = [(0,1,2), (3,4,5), (6,7,8), #horizontal
                           (0,3,6), (1,4,7), (2,5,8), #vert
                           (2,4,6), (0,4,8)]          #diag


    def move_added(self, spot):
        if self.state.find(str(spot)) > -1:
            return -1, -1, ''
        self.make_move(spot, 'P')
        computer_move = self.make_computer_move(self.state)
        self.make_move(computer_move[1], 'C')

        is_won = ''
        winning_moves = ''
        if self.is_won(self.state, 'C'):
            is_won = 'won'
            winning_moves = self.get_winning_moves()

        return computer_move[1], is_won, winning_moves

    def make_move(self, spot, piece):
        if len(self.state) > 0:
            self.state += ',' + str(spot) + piece
        else:
            self.state = str(spot) + piece
        self.save()
        return

    def make_computer_move(self, state, player = 'C'):
        next_player = self.player_toggle(player)
        unused_squares = self.get_unused_squares(state)
        #
        # end points for recursion
        #
        if self.is_won(state, next_player): #win
            if player == 'P':
                return (1, -1)
            else:
                return (-1, -1)
        if len(unused_squares) == 0: #tie
            return (0, -1)

        if player == 'C': #choose best square for computer
            best_score = -1
            best_square = -1
            for square in unused_squares:
                temp_state = state + ',' + str(square) +player
                score = self.make_computer_move(temp_state, next_player)
                if best_score < score[0]:
                    best_score = score[0]
                    best_square = square
            return (best_score, best_square)
        else:
            best_score = 1
            best_square = -1
            for square in unused_squares:
                temp_state = state + ',' + str(square) + player
                score = self.make_computer_move(temp_state, next_player)
                if best_score > score[0]:
                    best_score = score[0]
                    best_square = square
            return (best_score, best_square)

    def is_won(self, state, player):
        # 
        # tests to see if a player is occupying all 3 spots
        # in WINNING_COMBINATIONS
        #
        for combo in self.WINNING_COMBINATIONS:
            is_won = True
            for i in combo:
                if state.find(str(i) + player) == -1:
                    is_won = False
            if is_won:
                return True
        return False

    def get_winning_moves(self):
        for combo in self.WINNING_COMBINATIONS:
            is_winning_combo = True
            
            for i in combo:
                if self.state.find(str(i) + 'C') == -1:
                    is_winning_combo = False
            if is_winning_combo:
                return combo
        return

    
    def get_unused_squares(self, state):
        unused_squares = []
        for num in range(0,9):
            if state.find(str(num)) == -1:
                unused_squares.append(num)
        return unused_squares

    def player_toggle(self, player):
        return 'P' if player == 'C' else 'C'





        



