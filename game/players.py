"""
Players are defined their "play" method, which takes a game model
(or an object that proxies a game model, in such a way they aren't
allowed to perform any illegal actions).

They are expected to return an index that is their play.
"""
import random
from django.utils.module_loading import import_by_path


class AIPlayer(object):
    """
    The AI Player, Alpha Beta Pruning
    """

    def str_to_list(self, a):
        if a == " ":
            return None
        else:
            return a

    def play(self, game):
        # Find a spot on the board that's open.\\\
        self.game = game
        self.board = [self.str_to_list(a) for a in list(game.board)]
        type = game.next_player
        position = self._determine(type)
        return position

    def get_enemy(self, player):
        if player == 'X':
            return 'O'
        return 'X'

    def make_move(self, position, player):
        """place on square on the board"""
        self.board[position] = player

    def available_moves(self):
        """all available squares"""
        return [k for k, v in enumerate(self.board) if v is None]

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.board) if v == player]

    def _determine(self, player):
        a = -2
        choices = []
        moves = self.available_moves()
        if len(moves) == 9:
            return 4
        for move in moves:
            self.make_move(move, player)
            val = self.alphabeta(self.get_enemy(player), -2, 2)
            self.make_move(move, None)
            if val > a:
                a = val
                choices = [move]
            elif val == a:
                choices.append(move)
        return random.choice(choices)

    def is_game_over(self):
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' '
        """
        for wins in self.game.WINNING:
            # Create a tuple
            w = (self.board[wins[0]], self.board[wins[1]], self.board[wins[2]])
            if w == ('X', 'X', 'X'):
                return 'X'
            if w == ('O', 'O', 'O'):
                return 'O'
        return ' '

    def alphabeta(self, player, alpha, beta):
        if None not in self.board:
            who_won = self.is_game_over()
            if who_won == 'X':
                return -1
            elif who_won == ' ':
                return 0
            elif who_won == 'O':
                return 1
        for move in self.available_moves():
            self.make_move(move, player)
            val = self.alphabeta(self.get_enemy(player), alpha, beta)
            self.make_move(move, None)
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


def get_player(player_type):
    """
    This uses importlib to load the class.
    Since we don't have that many player types, you could hardcode types
    as well.
    """
    cls = import_by_path(player_type)
    return cls()
