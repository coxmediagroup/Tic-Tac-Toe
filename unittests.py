import unittest
from TicTacToe import TicTacToe

class test_TicTacToe(unittest.TestCase):
    def setUp(self):
        self.ttt = TicTacToe()
        
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
        
    def test_undo_move(self):
        self.ttt.make_move(self.ttt.COMPUTER, 0)
        self.ttt.make_move(self.ttt.HUMAN, 8)
        board = ["."] * 9
        board[0] = "x"
        self.assertTrue(self.ttt.undo_move(self.ttt.HUMAN, 8))
        self.assertEqual(board, self.ttt.board)
        self.assertEqual([], self.ttt.squares[self.ttt.HUMAN])
        self.assertFalse(self.ttt.undo_move(self.ttt.HUMAN, 0))
        
        free_squares = [x for x in range(1, 9)]
        self.assertEqual(set(self.ttt.free_squares), set(free_squares))
        self.assertEqual(self.ttt.turns, 1)
        
    def test_check_game_over(self):
        #test computer victory
        squares = [[0,1,2],[]]
        self.assertEqual(self.ttt.check_game_over(squares), (True, 1))
        
        #test human victory
        squares = [[],[2,5,8]]
        self.assertEqual(self.ttt.check_game_over(squares), (True, -1))
        
        #test tie
        #squares = [[4,1,8,6,5],[0,7,3,2]]
        self.ttt.make_move(self.ttt.COMPUTER,4)
        self.ttt.make_move(self.ttt.HUMAN,0)
        self.ttt.make_move(self.ttt.COMPUTER,1)
        self.ttt.make_move(self.ttt.HUMAN,7)
        self.ttt.make_move(self.ttt.COMPUTER,8)
        self.ttt.make_move(self.ttt.HUMAN,3)
        self.ttt.make_move(self.ttt.COMPUTER,6)
        self.ttt.make_move(self.ttt.HUMAN,2)
        self.ttt.make_move(self.ttt.COMPUTER,5)
        self.assertEqual(self.ttt.check_game_over(self.ttt.squares), (True, 0))

        #test no winner, no tie
        self.ttt.undo_move(self.ttt.COMPUTER, 5)
        self.assertEqual(self.ttt.check_game_over(self.ttt.squares), (False, None))
        
    def test_do_computer_turn(self):
        self.ttt.do_computer_turn()
        self.assertEqual(self.ttt.squares[self.ttt.COMPUTER], [4])
        
        self.ttt.do_computer_turn()
        self.assertEqual(len(self.ttt.squares[self.ttt.COMPUTER]), 2)
        self.assertEqual(self.ttt.board_control, self.ttt.HUMAN)
        
        
if __name__ == '__main__':
    unittest.main()