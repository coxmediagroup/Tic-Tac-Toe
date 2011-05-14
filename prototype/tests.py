import unittest
from tic_tac_toe import Board

class Board_test(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_board_size(self):
        self.assertEquals(self.board.size(), 9)

    def test_board_take_cell(self):
        self.assertEquals(self.board.get_cell(0), None)
        self.board.take_cell(0, "X")
        self.assertEquals(self.board.get_cell(0), "X")

if __name__ == "__main__":
    unittest.main()
