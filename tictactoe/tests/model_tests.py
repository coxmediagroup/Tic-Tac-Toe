from django.contrib.auth.models import User
from django.test import TestCase

from .. import models


class PositionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='default',
                                             password='password')
        self.game = models.Game(user=self.user)
        self.game.save()

    def test_new_game(self):
        self.assertEqual(self.game.positions.count(), 0)
        self.game.positions.create()

        self.assertEqual(self.game.positions.count(), 1)
        position = self.game.positions.get()
        self.assertEqual(position.state, 0)

    def test_make_play(self):
        self.game.positions.create()
        self.assertEqual(self.game.positions.count(), 1)
        position = self.game.positions.get()

        new_position = position.make_move('a3')
        self.game = models.Game.objects.get()
        self.assertEqual(self.game.positions.count(), 2)
        self.assertEqual(self.game.positions.latest(), new_position)
        self.assertEqual(new_position.state, 0b001000000)

    def test_repeated_plays_are_not_legal(self):
        position = self.game.positions.create()
        new_position = position.make_move('a3')
        self.assertEqual(self.game.positions.count(), 2)

        self.assertFalse(new_position.is_legal('a3'))
        with self.assertRaises(Exception):
            new_position.make_move('a3')

        self.assertEqual(self.game.positions.count(), 2)

    def test_out_of_bounds_is_illegal(self):
        position = self.game.positions.create()

        with self.assertRaises(Exception):
            position.make_move('b4')

        self.assertEqual(models.Position.objects.count(), 1)
