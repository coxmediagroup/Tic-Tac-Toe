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
        self.assertEqual(game.board, "    X    ")

    def test_priorities_horizontal(self):
        p1 = AIPlayer()
        game = Game(board="OO  X  X ",player_x=p1, player_o='human')
        game.play(p1.play(game))
        self.assertEqual("OOX X  X ", game.board)


    def test_priorities_diagonal(self):
        p1 = AIPlayer()
        game = Game(board="O X OX   ",player_x=p1, player_o='human')
        game.play(p1.play(game))
        self.assertEqual("O X OX  X", game.board)


    def test_priorities_vertical(self):
        p1 = AIPlayer()
        game = Game(board="O XO X   ",player_x=p1, player_o='human')
        game.play(p1.play(game))
        self.assertEqual("O XO X  X", game.board)