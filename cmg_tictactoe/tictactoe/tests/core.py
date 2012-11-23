from django.test import TestCase

from ..core import X, O, Grid, Player


class GridTestCase(TestCase):

    def test_positions(self):
        grid = Grid()
        self.assertItemsEqual(grid.positions(), [0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertItemsEqual(grid.positions(X), [])
        self.assertItemsEqual(grid.positions(O), [])
        grid = Grid(u'xo__x____')
        self.assertItemsEqual(grid.positions(), [2, 3, 5, 6, 7, 8])
        self.assertItemsEqual(grid.positions(X), [0, 4])
        self.assertItemsEqual(grid.positions(O), [1])

    def test_is_complete(self):
        self.assertFalse(Grid('_ox______').is_complete())
        self.assertTrue(Grid('xoxoxoxox').is_complete())

    def test_is_turn(self):
        grid = Grid()
        self.assertTrue(grid.is_turn(X))
        self.assertFalse(grid.is_turn(O))
        grid = Grid(u'xoxoxoxox')
        self.assertFalse(grid.is_turn(X))
        self.assertFalse(grid.is_turn(O))
        grid = Grid(u'xoxoxoxo_')
        self.assertTrue(grid.is_turn(X))
        self.assertFalse(grid.is_turn(O))
        grid = Grid(u'xox_xoxo_')
        self.assertFalse(grid.is_turn(X))
        self.assertTrue(grid.is_turn(O))


class PlayerTestCase(TestCase):

    def test_complete_winning_sequence(self):
        """ Test a sample of the winning sequences. """
        player = Player()
        self.assertIsNone(player._complete_winning_sequence(player.x))
        player.grid = Grid(u'_xx_oo___')
        self.assertEqual(player._complete_winning_sequence(player.x), 0)
        player.grid = Grid(u'_oox_x___')
        self.assertEqual(player._complete_winning_sequence(player.x), 4)
        player.grid = Grid(u'_xx___oo_')
        self.assertEqual(player._complete_winning_sequence(player.o), 8)
        player.grid = Grid(u'xoox_____')
        self.assertEqual(player._complete_winning_sequence(player.x), 6)
        player.grid = Grid(u'_xo_x___o')
        self.assertEqual(player._complete_winning_sequence(player.x), 7)
        player.grid = Grid(u'_x_x_o__o')
        self.assertEqual(player._complete_winning_sequence(player.o), 2)
        player.grid = Grid(u'xo____o_x')
        self.assertEqual(player._complete_winning_sequence(player.x), 4)
        player.grid = Grid(u'xoxox___o')
        self.assertEqual(player._complete_winning_sequence(player.x), 6)

    def test_form_fork(self):
        """ Test a sample of the possible fork setups. """
        player = Player()
        self.assertIsNone(player._form_fork(player.x))
        player.grid = Grid(u'_x__ox_o_')
        self.assertEqual(player._form_fork(player.x), 2)
        player.grid = Grid(u'_o_xo__x_')
        self.assertEqual(player._form_fork(player.x), 6)
        player.grid = Grid(u'o__x__ox_')
        self.assertEqual(player._form_fork(player.x), 4)
        player.grid = Grid(u'_xox__o__')
        self.assertEqual(player._form_fork(player.x), 4)

    def test_play_in_center(self):
        player = Player(grid=Grid(u'_________'))
        self.assertEqual(player.play_in_center(), player.grid.CENTER)
        player.grid = Grid(u'xoxo_oxox')
        self.assertEqual(player.play_in_center(), player.grid.CENTER)
        player.grid = Grid(u'oxoxox_x_')
        self.assertIsNone(player.play_in_center())

    def test_play_in_corner_opposite_opponent(self):
        player = Player(grid=Grid(u'_________'))
        self.assertIsNone(player.play_in_corner_opposite_opponent())
        player.grid = Grid(u'o_x______')
        self.assertEqual(player.play_in_corner_opposite_opponent(), 8)
        player.grid = Grid(u'oxoxox___')
        self.assertIn(player.play_in_corner_opposite_opponent(), [6, 8])
        player.grid = Grid(u'oxox_xoxo')
        self.assertIsNone(player.play_in_corner_opposite_opponent())

    def test_play_in_corner(self):
        player = Player(grid=Grid(u'_________'))
        self.assertIn(player.play_in_corner(), player.grid.CORNERS)
        player.grid = Grid(u'xo_oxoxxo')
        self.assertIn(player.play_in_corner(), player.grid.CORNERS)
        player.grid = Grid(u'o_o___x_x')
        self.assertIsNone(player.play_in_corner())

    def test_play_on_side(self):
        player = Player(grid=Grid(u'_________'))
        self.assertIn(player.play_on_side(), player.grid.SIDES)
        player.grid = Grid(u'x_xo_ox_x')
        self.assertIn(player.play_on_side(), player.grid.SIDES)
        player.grid = Grid(u'_x_x_o_o_')
        self.assertRaises(IndexError, player.play_on_side)
