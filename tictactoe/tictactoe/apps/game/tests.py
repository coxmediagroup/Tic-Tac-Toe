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
                print game
                assert game.winner != game.player
                return

            if next_player == game.computer:
                game.computer_move()
                _play(game, game.player)
            else:
                for tile in game.available_tiles:
                    this_game = deepcopy(game)
                    this_game.player_move(tile)
                    _play(this_game, game.computer)

        _play(TicTacToe(), TicTacToe.player)                  # user starts game
        _play(TicTacToe(), TicTacToe.computer)                # computer starts game