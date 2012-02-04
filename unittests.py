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
        
    def test_move_possible(self):
        self.assertTrue(self.ttt.move_possible(3))
        self.ttt.make_move(self.ttt.COMPUTER, 3)
        self.assertFalse(self.ttt.move_possible(3))
    
    def test_make_move(self):
        self.ttt.make_move(self.ttt.COMPUTER, 0)
        self.ttt.make_move(self.ttt.HUMAN, 4)
        
        board = ["."] * 9
        board[0] = "x"
        board[4] = "o"
        self.assertEqual(self.ttt.board, board)
        
        human = [4]
        computer = [0]
        self.assertEqual(human, self.ttt.squares[self.ttt.HUMAN])
        self.assertEqual(computer, self.ttt.squares[self.ttt.COMPUTER])
        
        free_squares = [x for x in range(9)]
        free_squares.remove(0)
        free_squares.remove(4)
        self.assertEqual(free_squares, self.ttt.free_squares)
        
        self.assertEqual(2, self.ttt.turns)
        
if __name__ == '__main__':
    unittest.main()