import unittest
import TicTacToe

class test_TicTacToe(unittest.TestCase):
    def setUp(self):
        self.ttt = TicTacToe.TicTacToe()
        
    def test_reset(self):
        board = ["."] * 9
        squares = [[],[]]
        free_squares = [x for x in range(9)]
        game_over = False
        turns = 0
        self.ttt.reset_board()
        self.assertEqual(self.ttt.board, board)
        self.assertEqual(self.ttt.squares, squares)
        self.assertEqual(self.ttt.free_squares, free_squares)
        self.assertEqual(self.ttt.game_over, game_over)
        self.assertEqual(self.ttt.turns, turns)
        
if __name__ == '__main__':
    unittest.main()