import unittest
import TicTacToeLib


class TicTacToeLibTests(unittest.TestCase):

    def setUp(self):
        self.testboard=[TicTacToeLib.BLANK]*TicTacToeLib.GAME_BOARD_SIZE

    def testGetBoard(self):
        board = TicTacToeLib.Board()
        self.assertListEqual(self.testboard, board.getGameBoard())


if __name__ == "__main__":
    unittest.main()