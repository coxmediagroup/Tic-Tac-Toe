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
        self.assertEqual(position.state, ' '*9)
        self.assertEqual(position.player(), 'x')

    def test_new_position(self):
        self.game.positions.create()
        self.assertEqual(self.game.positions.count(), 1)
        position = self.game.positions.get()

        new_position = position.new((0, 2))
        self.game = models.Game.objects.get()
        self.assertEqual(self.game.positions.count(), 2)
        self.assertEqual(self.game.positions.latest(), new_position)
        self.assertEqual(new_position.state, '  x      ')

    def test_repeated_plays_are_not_legal(self):
        position = self.game.positions.create()
        new_position = position.new((0, 2))
        self.assertEqual(self.game.positions.count(), 2)

        self.assertFalse(new_position.is_legal((0, 2)))
        with self.assertRaises(Exception):
            new_position.new((0, 2))

        self.assertEqual(self.game.positions.count(), 2)

    def test_out_of_bounds_is_illegal(self):
        position = self.game.positions.create()

        with self.assertRaises(Exception):
            position.new('b4')

        self.assertEqual(models.Position.objects.count(), 1)

    def test_empty_is_not_won(self):
        position = self.game.positions.create()

        self.assertFalse(position.is_won())

    def test_column_is_won(self):
        position = self.game.positions.create()
        position = position.new((0, 2))
        self.assertFalse(position.is_won())
        position = position.new((0, 1))
        self.assertFalse(position.is_won())
        position = position.new((1, 2))
        self.assertFalse(position.is_won())
        position = position.new((1, 1))
        self.assertFalse(position.is_won())
        position = position.new((2, 2))
        self.assertTrue(position.is_won())

    def test_row_is_won(self):
        position = self.game.positions.create()
        position = position.new((0, 2))
        self.assertFalse(position.is_won())
        position = position.new((1, 2))
        self.assertFalse(position.is_won())
        position = position.new((0, 1))
        self.assertFalse(position.is_won())
        position = position.new((1, 1))
        self.assertFalse(position.is_won())
        position = position.new((0, 0))
        self.assertTrue(position.is_won())

    def test_diagonal_is_won(self):
        position = self.game.positions.create()
        position = position.new((0, 2))
        self.assertFalse(position.is_won())
        position = position.new((1, 2))
        self.assertFalse(position.is_won())
        position = position.new((1, 1))
        self.assertFalse(position.is_won())
        position = position.new((2, 2))
        self.assertFalse(position.is_won())
        position = position.new((2, 0))
        self.assertTrue(position.is_won())
