import random

from django.db import models

# Global variables
SIGNS = ('X', 'O')
WIN_MOVES = ([0, 1, 2], [3, 4, 5], [6, 7, 8],
             [0, 3, 6], [1, 4, 7], [2, 5, 8],
             [0, 4, 8], [2, 4, 6])


class Player(models.Model):

    sign = models.CharField(max_length=1)

    def __init__(self, sign):
        if sign in SIGNS:
            self.sign = sign

    def __unicode__(self):
        return self.sign


class TicTacToe(models.Model):

    def __init__(self, enemy, squares=[]):
        if len(squares) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = squares
        self.pc_player = Player(get_enemy(enemy.sign))

    def possible_moves(self):
        """
        Return the postions available in the grid
        that one player can use.
        """
        return [k for k, v in enumerate(self.squares) if v is None]

    def available_combos(self, player):
        """
        What combos are available?
        """
        return self.possible_moves() + self.player_squares(player)

    def complete(self):
        """
        Check if the game is over.
        """
        if None not in [v for v in self.squares]:
            return True
        if self.winner() is not None:
            return True
        return False

    def winner(self):
        """
        Check if a user won the game
        and it returns it if it did.
        """
        for player in SIGNS:
            positions = self.player_squares(player)
            for combo in WIN_MOVES:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None

    def winner_label(self):
        if self.X_win():
            return "Winner is X"
        elif self.tied():
            return "Draw"
        elif self.O_win():
            return "Winner is O"
        return None

    def player_squares(self, player):
        """
        Return the squares that a particular user
        has played.
        """
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """
        Make the move of the player in the squares
        of the game.
        """
        self.squares[position] = player

    def X_win(self):
        return self.winner() == 'X'

    def O_win(self):
        return self.winner() == 'O'

    def tied(self):
        """
        Return true is the game is over and there is no winner
        """
        return self.complete() is True and self.winner() is None

    def alpha_beta(self, node, player, alpha, beta):
        """
        Using the algorithm Alpha Beta Pruning as a search
        algorithm.

        Idea = Minimizing the possible loss in a worst case scenario

        http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

        """
        if node.complete():  # node is a terminal node
            sign = self.pc_player.sign
            if node.X_win():
                return 1 if sign == 'X' else -1
            elif node.tied():
                return 0
            elif node.O_win():
                return -1 if sign == 'X' else 1

        for move in node.possible_moves():
            node.make_move(move, player)
            val = self.alpha_beta(node, get_enemy(player), alpha, beta)
            node.make_move(move, None)
            if player == self.pc_player.sign:
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha

        if player == self.pc_player.sign:
            return alpha
        else:
            return beta

    def next_move(self):
        """
        Calculate the possible moves using alpha beta pruning
        and choosing a random move in the result.
        """
        a = -2
        choices = []
        if len(self.possible_moves()) == 9:
            return 4
        for move in self.possible_moves():
            self.make_move(move, self.pc_player.sign)
            val = self.alpha_beta(self, get_enemy(self.pc_player.sign), -2, 2)
            self.make_move(move, None)
            if val > a:
                a = val
                choices = [move]
            elif val == a:
                choices.append(move)
        value = random.choice(choices)
        self.make_move(value, self.pc_player.sign)


def get_enemy(player):
    if player == 'O':
        return 'X'
    return 'O'
