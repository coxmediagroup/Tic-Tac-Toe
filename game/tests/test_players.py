import random
from django.test import TestCase

from game.models import Game
from game.players import get_player, RandomPlayer


class RandomPlayerTest(TestCase):
    def test_import(self):
        p = get_player("game.players.RandomPlayer")
        self.assertEqual(type(p), RandomPlayer)

    def test_random(self):
        "Basic testing."

        random.seed(0)  # For testing
        game = Game()
        p1 = RandomPlayer()

        game.play(p1.play(game))
        self.assertEqual(game.board, "       X ")
