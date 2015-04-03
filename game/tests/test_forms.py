import random
from django.test import TestCase

from game.forms import NewGameForm


class NewGameFormTest(TestCase):
    def test_player_valid(self):
        form = NewGameForm({
            'player1': 'game.players.AIPlayer',
            'player2': 'human'
        })
        self.assertTrue(form.is_valid())

    def test_player_invalid(self):
        form = NewGameForm({
            'player1': '',
            'player2': 'foobar'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'player1': ['This field is required.'],
            'player2': ['Unknown player type: foobar']
        })

    def test_create(self):
        "Tests that create returns a model with the players assigned."
        random.seed(1)

        form = NewGameForm({
            'player1': 'game.players.AIPlayer',
            'player2': 'human'
        })
        self.assertTrue(form.is_valid())
        game = form.create()
        self.assertEqual(game.board, "         ")
        self.assertEqual(game.player_x, "human")
        self.assertEqual(game.player_o, "game.players.AIPlayer")
