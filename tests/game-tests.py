import unittest

import game


class TestMoves(unittest.TestCase):

    def setUp(self):
        pass

    def test_ai_move_one(self):
        actual = game.ai_move_one()
        expected = ['c1', 'c3', 'c7', 'c9']
        self.assertIn(actual, expected)
