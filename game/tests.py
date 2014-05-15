"""
Tic-Tac-Toe unit tests
"""

from game.models import Game
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client, ClientHandler, RequestFactory

from game.views import new_X, new_O, index


class TestUrls(TestCase):
    def test_game(self):
        client = Client()
        response = client.get(reverse('game:index'))
        self.assertEqual(response.status_code, 200)


class TestNewXSetup(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_X(self):
        response = self.client.get(reverse('game:newX'))
        self.assertEqual(response.status_code, 302)
        self.assert_('game_id' in self.client.session)
        game_id = self.client.session.get('game_id', None)
        game = Game.objects.get(pk=game_id)
        self.assertListEqual(game.board,
                             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])


class TestNewOSetup(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_O(self):
        response = self.client.get(reverse('game:newO'))
        self.assertEqual(response.status_code, 302)
        self.assert_('game_id' in self.client.session)
        game_id = self.client.session.get('game_id', None)
        game = Game.objects.get(pk=game_id)
        self.assertListEqual(game.board,
                             ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])


class TestGameMethods(TestCase):
    def setUp(self):
        self.game = Game(symbol='O')

    def test_place_win(self):
        self.game.board = [
            'X', 'X', ' ',
            'O', 'O', ' ',
            ' ', ' ', ' ' ]
        self.game.place_win()
        self.assertListEqual(self.game.board, [
            'X', 'X', 'X',
            'O', 'O', ' ',
            ' ', ' ', ' ' ])

    def test_place_block(self):
        self.game.board = [
            'X', 'X', 'O',
            ' ', 'O', ' ',
            ' ', ' ', ' ' ]
        self.game.place_block()
        self.assertListEqual(self.game.board, [
            'X', 'X', 'O',
            ' ', 'O', ' ',
            'X', ' ', ' ' ])

    def test_place_fork(self):
        self.game.board = [
            'X', ' ', ' ',
            ' ', 'O', ' ',
            'O', ' ', 'X' ]
        x = self.game.place_fork()
        self.assertEqual(x, 2)
        self.assertListEqual(self.game.board, [
            'X', ' ', 'X',
            ' ', 'O', ' ',
            'O', ' ', 'X' ])

    def test_place_fork_block(self):
        self.game.board = [
            'X', ' ', ' ',
            ' ', 'O', ' ',
            'O', ' ', 'X' ]
        x = self.game.place_fork()
        self.assertEqual(x, 2)
        self.assertListEqual(self.game.board, [
            'X', ' ', 'X',
            ' ', 'O', ' ',
            'O', ' ', 'X' ])

    def test_place_center(self):
        self.game.board = [
            'O', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' ]
        x = self.game.place_center()
        self.assertEqual(x, 4)
        self.assertListEqual(self.game.board, [
            'O', ' ', ' ',
            ' ', 'X', ' ',
            ' ', ' ', ' ' ])

    def test_place_opposite_corner(self):
        self.game.board = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            'O', ' ', ' ' ]
        x = self.game.place_opposite_corner()
        self.assertEqual(x, 2)
        self.assertListEqual(self.game.board, [
            ' ', ' ', 'X',
            ' ', ' ', ' ',
            'O', ' ', ' ' ])

    def test_place_empty_corner(self):
        self.game.board = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' ]
        x = self.game.place_empty_corner()
        self.assertEqual(x, 0)
        self.assertListEqual(self.game.board, [
            'X', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' ])

    def test_place_empty_side(self):
        self.game.board = [
            ' ', ' ', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' ]
        x = self.game.place_empty_side()
        self.assertEqual(x, 1)
        self.assertListEqual(self.game.board, [
            ' ', 'X', ' ',
            ' ', ' ', ' ',
            ' ', ' ', ' ' ])

    def test_place_empty(self):
        self.game.board = [
            'X', 'X', 'O',
            ' ', 'X', 'O',
            'O', 'O', 'X' ]
        x = self.game.place_empty_side()
        self.assertEqual(x, 3)
        self.assertListEqual(self.game.board, [
            'X', 'X', 'O',
            'X', 'X', 'O',
            'O', 'O', 'X' ])
