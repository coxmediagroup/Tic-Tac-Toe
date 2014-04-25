"""Tests for the ``logic`` module."""
import unittest

from . import logic


class AITest(unittest.TestCase):

    def test_first_move_o_responds_center_with_corner(self):
        """If AI is O, and X took center, AI takes a corner."""
        board = [
            '   ',
            ' X ',
            '   ',
        ]

        _, ai_response = logic.get_ai_move(board)
        self.assertEqual((0, 0), ai_response)

    def test_first_move_o_responds_edge_with_center(self):
        """If AI is O, and X didn't take center, takes the center."""
        board = [
            'X  ',
            '   ',
            '   ',
        ]

        _, ai_response = logic.get_ai_move(board)
        self.assertEqual((1, 1), ai_response)

        board = [
            ' X ',
            '   ',
            '   ',
        ]

        _, ai_response = logic.get_ai_move(board)
        self.assertEqual((1, 1), ai_response)

    def test_board_with_first_move_gets_o_response(self):

        board = [
            'X  ',
            '   ',
            '   ',
        ]

        ai_piece, _ = logic.get_ai_move(board)
        self.assertEqual('O', ai_piece)