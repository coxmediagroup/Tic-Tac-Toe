import unittest
from tic_tac_toe import Board

class Board_test(unittest.TestCase):
    def setUp(self):
        self.board = Board()


    def test_board(self):
        self.assertEquals(self.board.size, 9)

if __name__ == "__main__":
    unittest.main()
