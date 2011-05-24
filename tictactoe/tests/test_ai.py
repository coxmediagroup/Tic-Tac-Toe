import unittest2 as unittest

from tictactoe import ai
from tictactoe.board import Board


class TestAi(unittest.TestCase):

    def test_get_move_scores(self):
        board = Board()
        board.add_move(board.o, 0)
        move_scores = ai.get_move_scores(board, board.x)
        expected = [
            (1, -1), (3, -1), (5, -1), (7, -1), (2, 0), (4, 0), (6, 0), (8, 0)]
        self.assertEqual(move_scores, expected, 'Invalid move scores')

    def test_get_move_position(self):
        board = Board()
        board.add_move(board.o, 0)
        move = ai.get_move_position(board, board.x)
        self.assertEqual(move, 8, 'Incorrect move position')
