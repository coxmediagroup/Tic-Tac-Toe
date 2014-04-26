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

    def test_o_responds_to_diagonal_trap_with_x_centered(self):
        """The AI playing O blocks a diagonal trap with X at the center."""
        board = [
            '  X',
            ' X ',
            '0  ',
        ]

        _, ai_response = logic.get_ai_move(board)

        took_corner = ai_response == (0, 0) or ai_response == (2, 2)
        self.assertTrue(took_corner, ai_response)

        board = [
            'X  ',
            ' X ',
            '  0',
        ]

        _, ai_response = logic.get_ai_move(board)

        took_corner = ai_response == (0, 2) or ai_response == (2, 0)
        self.assertTrue(took_corner, ai_response)

        board = [
            '0  ',
            ' X ',
            '  X',
        ]

        _, ai_response = logic.get_ai_move(board)

        took_corner = ai_response == (0, 2) or ai_response == (2, 0)
        self.assertTrue(took_corner, ai_response)

    def test_o_responds_to_diagonal_trap_with_o_centered(self):
        """The AI playing O blocks a diagonal trap with O at the center."""
        board = [
            '  X',
            ' O ',
            'X  ',
        ]

        _, ai_response = logic.get_ai_move(board)

        took_edge = ai_response in ((0, 1), (1, 0), (2, 1), (1, 2))
        self.assertTrue(took_edge, ai_response)

        board = [
            'X  ',
            ' O ',
            '  X',
        ]

        _, ai_response = logic.get_ai_move(board)

        took_edge = ai_response in ((0, 1), (1, 0), (2, 1), (1, 2))
        self.assertTrue(took_edge, ai_response)

    def test_tries_to_block_diagonal_victory(self):
        """If opponent would win next turn on a diagonal, AI blocks it."""
        board = [
            'O  ',
            ' X ',
            'X  ',
        ]

        _, ai_response = logic.get_ai_move(board)

        self.assertEqual((0, 2), ai_response)

        board = [
            '  O',
            ' X ',
            '  X',
        ]

        _, ai_response = logic.get_ai_move(board)

        self.assertEqual((0, 0), ai_response)

    def test_tries_to_block_vertical_victory(self):
        """If opponent would win next turn on a vertical, AI blocks it."""
        board = [
            'OXO',
            ' X ',
            'X  ',
        ]

        _, ai_response = logic.get_ai_move(board)

        self.assertEqual((2, 1), ai_response)