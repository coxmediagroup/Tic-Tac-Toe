"""Tests for the ``gamestate`` module."""
import unittest

from .. import gamestate


class GameStateTest(unittest.TestCase):

    def test_finds_victory_horizontally(self):
        board = [
            'XXX',
            ' OO',
            '   ',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('X', info.winner)
        self.assertEqual({(0, 0), (0, 1), (0, 2)}, set(info.win_cells))