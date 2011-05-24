import unittest2 as unittest

from tictactoe import ai
from tictactoe.board import Board


class TestAi(unittest.TestCase):

    def test_get_move_scores(self):
        board = Board()
        board.add_move(board.o, 0)
        move_scores = ai.get_move_scores(board, board.x)
        expected = [(1, -1), (2, -1), (3, -1), (4, 0),
                    (5, -1), (6, -1), (7, -1), (8, -1)]
        self.assertItemsEqual(move_scores, expected, 'Invalid move scores')

    def test_get_move_position(self):
        board = Board()
        board.add_move(board.o, 0)
        move = ai.get_move_position(board, board.x)
        self.assertEqual(move, 4, 'Incorrect move position')

    def test_get_move_position_for_obvious_play(self):
        board = Board(state=[x for x in 'xx      o'])
        move = ai.get_move_position(board, board.o)
        self.assertEqual(move, 2, 'Incorrect move position')
