import unittest

import game


class TestMoveCalc(unittest.TestCase):

    def setUp(self):
        pass

    def test_first_ai_move(self):
        actual = game.calc_ai_first()
        expected = ['c1', 'c3', 'c7', 'c9']
        self.assertIn(actual, expected)
