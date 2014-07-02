import random
from django.utils import unittest
from .game import TicTacToe


class TestGame(unittest.TestCase):
    """
    Test the game logic to ensure the player never wins
    """
    def test_game_play(self):
        def _play(game, next_player):
            while True:
                if next_player == game.computer:
                    game.computer_move()
                    next_player = game.player
                else:
                    game.player_move(random.choice(game.available_tiles))
                    next_player = game.computer

                if game.winner:
                    print "[Winner: {winner}, {board}]".format(winner=game.winner, board=game.board)
                    assert game.winner != game.player
                    break


        _play(TicTacToe(), TicTacToe.computer)                  # user starts game
        _play(TicTacToe(user_starts=False), TicTacToe.player)   # computer starts game