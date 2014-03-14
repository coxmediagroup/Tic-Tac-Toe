import unittest
from tic_tac_toe import *

class TicTacTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_throws_exception_on_cheating(self):
        self.board.play("0", 1, 1)
        with self.assertRaises(PlayException):
            self.board.play("X", 1, 1)

if __name__ == '__main__':
    unittest.main()