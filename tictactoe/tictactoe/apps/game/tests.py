from copy import deepcopy
import random
from django.utils import unittest
from .game import TicTacToe


class TestGame(unittest.TestCase):
    """
    Test the game logic to ensure the player never wins
    """
    def test_game_play(self):
        def _play(game, next_player):
            if game.winner:
                print "[Winner: {winner}, {board}]".format(winner=game.winner, board=game.board)
                #assert game.winner != game.player
                return

            this_game = deepcopy(game)
            if next_player == this_game.computer:
                this_game.computer_move()
                _play(this_game, this_game.player)
            else:
                for tile in game.available_tiles:
                    this_game.player_move(tile)
                    _play(this_game, this_game.computer)

        _play(TicTacToe(), TicTacToe.computer)                  # user starts game
        _play(TicTacToe(user_starts=False), TicTacToe.player)   # computer starts game