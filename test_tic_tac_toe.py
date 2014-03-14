import unittest
from tic_tac_toe import *

class TicTacBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_throws_exception_on_cheating(self):
        self.board.play("0", 1, 1)
        with self.assertRaises(PlayException):
            self.board.play("X", 1, 1)

class TicTacPlayer(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player1 = AIPlayer(self.board, "X", "0")

    def test_player_gets_all_moves(self):
        self.assertEqual(len(self.player1._available_moves_()), 9)

    def test_player_score_moves(self):
        self.assertEqual(self.player1._score_move_(1,1), 4)
        
if __name__ == '__main__':
    unittest.main()