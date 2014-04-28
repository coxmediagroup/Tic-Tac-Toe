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

        board = [
            ' OO',
            'XXX',
            '   ',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('X', info.winner)
        self.assertEqual({(1, 0), (1, 1), (1, 2)}, set(info.win_cells))

        board = [
            ' XX',
            '   ',
            'OOO',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('O', info.winner)
        self.assertEqual({(2, 0), (2, 1), (2, 2)}, set(info.win_cells))

    def test_finds_victory_diagonally(self):
        board = [
            'XOX',
            ' XO',
            'X O',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('X', info.winner)
        self.assertEqual({(0, 2), (1, 1), (2, 0)}, set(info.win_cells))

        board = [
            'O X',
            'XO ',
            'X O',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('O', info.winner)
        self.assertEqual({(0, 0), (1, 1), (2, 2)}, set(info.win_cells))

    def test_finds_victory_vertically(self):
        board = [
            'XO ',
            'XO ',
            'X  ',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('X', info.winner)
        self.assertEqual({(0, 0), (1, 0), (2, 0)}, set(info.win_cells))

        board = [
            ' XO',
            'XXO',
            '  O',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.VICTORY, info.state)
        self.assertEqual('O', info.winner)
        self.assertEqual({(0, 2), (1, 2), (2, 2)}, set(info.win_cells))

    def test_empty_board_is_incomplete(self):
        board = [
            '   ',
            '   ',
            '   ',
        ]

        info = gamestate.check_board(board)

        self.assertEqual(gamestate.INCOMPLETE, info.state)