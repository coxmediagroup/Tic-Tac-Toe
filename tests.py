'''
Created on Nov 16, 2013

@author: mo
'''
import unittest
from Board import TicTacToe_Board
from ComputerPlayer import ComputerPlayer
from utils import debug_print as d_pr

from main import StartNewGame

class Test(unittest.TestCase):


    def setUp(self):
        self.the_board = TicTacToe_Board()

        
    def tearDown(self):
        pass

    #these may be impossible boards, but still it tests the win detector
    
    def test_these_should_win_for_x(self):
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static( [ ['x', 'x', 'x'], 
                                                          ['o', 'x', 'o'], 
                                                          ['o', 'x', 'o']]), 'x', "should return x")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                        ['x', 'o', 'o'],
                                                        ['o', 'x', 'o'],
                                                        ['x', 'o', 'x']
                                                        
                                                        
                                                        ]) , 'x', 'should return x')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                       ['o','x', 'o'],
                                                       ['x', 'x', 'x'],
                                                       ['-', '-', '-']
                                                       ]), 'x', 'should return x'
                                                       )
        
        
        
    def test_these_should_win_for_o(self):
        
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static( [ ['o', 'x', 'o'], 
                                                          ['o', 'x', 'x'], 
                                                          ['o', 'o', 'x']]), 'o', "should return o")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                        ['x', 'o', '-'],
                                                        ['o', 'o', 'o'],
                                                        ['o', 'x', 'x']
                                                        
                                                        
                                                        ]) , 'o', 'should return o')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                       ['o','x', 'o'],
                                                       ['x', 'o', 'x'],
                                                       ['-', '-', 'o']
                                                       ]), 'o', 'should return o'
                                                       )
        


    def test_these_should_win_for_nobody(self):
        
                
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static( [ ['x', 'x', '-'], 
                                                          ['o', '-', 'o'], 
                                                          ['o', '-', 'o']]), None, "should return None")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                        ['-', '-', '-'],
                                                        ['-', '-', '-'],
                                                        ['x', 'o', 'x']
                                                        
                                                        
                                                        ]) , None, 'should return None')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard_static([
                                                       ['o','x', 'o'],
                                                       ['-', '-', 'x'],
                                                       ['-', 'o', 'o']
                                                       ]), None, 'should return None'
                                                       )
        
    def test_make_move(self):
        
        self.the_board.board_array=[ ['x', '-', 'x'],
                               ['o', '-', 'o'],
                               ['o', 'x', '-']
                               ]
        
        self.the_board.whose_turn='o'
        
        self.the_board.MakeMove([1,1])
        
        self.assertEqual(self.the_board.board_array[1][1], 'o', "should be an o")
        
        self.assertEqual(self.the_board.whose_turn, 'x', 'turn should change')
        
        

    def test_computer_player_get_outcome(self):
        
        comp_player = ComputerPlayer('x', self.the_board)
        
        self.the_board.human_player_x_or_o = 'o'
        self.the_board.c_player_x_or_o = 'x'
        
        
        self.the_board.board_array = [ ['-', '-', 'x'],
                                       ['-', 'o', '-'],
                                       ['-', '-', '-']
                               ]
        self.the_board.whose_turn = 'x'
        
        move_seq_1 = [ {'player': 'x', 'move' : [0,1] }, {'player': 'o', 'move' :  [2,1]}, {'player': 'x', 'move': [0,0]} ]
        
        out=self.the_board.GetOutcomeOfMoveSequence(move_seq_1)
        
        self.assertEqual(out, 'x', 'x should win: outcome should be x')
        
        
        move_seq_2 = [{'player': 'x', 'move' : [0,1] }, {'player': 'o', 'move' :  [2,1]}]
        
        out = self.the_board.GetOutcomeOfMoveSequence(move_seq_2)
        self.assertEqual(out, None, 'no one should win: outcome will be None')

        move_seq_3 = [ {'player': 'x', 'move' : [0,1] }, {'player': 'o', 'move' : [0,0] }, {'player': 'x', 'move' :  [2,1]},
                      {'player': 'o', 'move' : [2,2] }
                      ]
        
        out = self.the_board.GetOutcomeOfMoveSequence(move_seq_3)
        
        self.assertEqual(out, 'o', 'o should win')
        
    
    def test_get_winning_moves_for_opponent(self):
        
        comp_player = ComputerPlayer('x', self.the_board)
        
        self.the_board.human_player_x_or_o = 'o'
        self.the_board.c_player_x_or_o = 'x'
        
        
        self.the_board.board_array = [ ['x', '-', 'x'],
                                       ['-', 'o', '-'],
                                       ['o', 'o', '-']
                               ]
        self.the_board.whose_turn = 'x'
        
        winning_moves=self.the_board.GetWinningMovesFor( 'human')
        
        d_pr(winning_moves)
        self.assertIn([0,1], winning_moves)
        self.assertIn([2,2], winning_moves)
        
        comp_player = ComputerPlayer('o', self.the_board)
        
        self.the_board.human_player_x_or_o = 'x'
        self.the_board.c_player_x_or_o = 'o'
        
        
        self.the_board.board_array = [ ['x', '-', 'x'],
                                       ['-', 'o', '-'],
                                       ['o', 'o', '-']
                               ]
        self.the_board.whose_turn = 'o'
        
        winning_moves=self.the_board.GetWinningMovesFor( 'human')
        
        d_pr(winning_moves)
        self.assertIn([0,1], winning_moves)
        
        
    
    def test_get_threatening_moves(self):
        
        comp_player = ComputerPlayer('x', self.the_board)
        
        self.the_board.human_player_x_or_o = 'o'
        self.the_board.c_player_x_or_o = 'x'
        
        
        self.the_board.board_array = [ ['-', '-', 'x'],
                                       ['-', 'o', '-'],
                                       ['o', '-', '-']
                               ]
        self.the_board.whose_turn = 'x'
        
        threatening_moves=comp_player.GetThreateningMovesWithoutTraps(self.the_board.GetEmptySquares())
        
       
        self.assertIn([0,0], threatening_moves)
        self.assertIn([2,2], threatening_moves)
       
        d_pr('threats without traps: ' + str(threatening_moves))
        
        self.assertEqual(len(threatening_moves), 2)
        
        
        
        
        
        self.the_board.human_player_x_or_o = 'o'
        self.the_board.c_player_x_or_o = 'x'
        
        
        self.the_board.board_array = [ ['-', '-', 'o'],
                                       ['-', 'x', '-'],
                                       ['o', '-', '-']
                               ]
        self.the_board.whose_turn = 'x'
        
        threatening_moves=comp_player.GetThreateningMovesWithoutTraps(self.the_board.GetEmptySquares())
        
       
        self.assertIn([0,1], threatening_moves)
        self.assertIn([2,1], threatening_moves)
        self.assertIn([1,0], threatening_moves)
        self.assertIn([1,2], threatening_moves)
        
        
        
        d_pr('threats without traps: ' + str(threatening_moves))
        
        self.assertEqual(len(threatening_moves), 4)
        
    
    
    
    def test_algorithm_by_playing_large_num_of_random_games(self):
        
        NUM_GAMES = 10
        #NUM_GAMES=100000 # this works but takes a long time
        NUM_GAMES=10
        
        for i in range(0, NUM_GAMES + 1):
            win_result = StartNewGame(UseRandom=True)
            
            self.assertTrue(win_result == 'Computer' or win_result == 'Tie')
        
    
    def test_print(self):
        
                
        self.the_board.board_array = [ ['-', '-', 'x'],
                                       ['-', 'o', '-'],
                                       ['x', 'o', '-']]
        
        self.the_board.PrintBoardToConsole()
    
    
    def test_empty_squares(self):
        pass
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
