import random
from django.test import TestCase

from game.models import Game
from game.players import get_player, AIPlayer


class AIPlayerTest(TestCase):
    def test_import(self):
        p = get_player("game.players.AIPlayer")
        self.assertEqual(type(p), AIPlayer)

    def test_random(self):
        "Basic testing."

        random.seed(0)  # For testing
        game = Game()
        p1 = AIPlayer()

        game.play(p1.play(game))
        self.assertEqual(game.board, "       X ")
