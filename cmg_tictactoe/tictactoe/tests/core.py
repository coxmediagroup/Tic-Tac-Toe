from django.test import TestCase

from ..core import Grid, Player


class GridTestCase(TestCase):

    def test_is_complete(self):
        self.assertFalse(Grid('_ox______').is_complete())
        self.assertTrue(Grid('xoxoxoxox').is_complete())


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
        # FIXME: Write tests for this.
        pass

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
