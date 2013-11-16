'''
Created on Nov 16, 2013

@author: mo
'''
import unittest
from Board import TicTacToe_Board

class Test(unittest.TestCase):


    def setUp(self):
        self.the_board = TicTacToe_Board()

        
    def tearDown(self):
        pass

    #these may be impossible boards, but still it tests the win detector
    
    def test_these_should_win_for_x(self):
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard( [ ['x', 'x', 'x'], 
                                                          ['o', 'x', 'o'], 
                                                          ['o', 'x', 'o']]), 'x', "should return x")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                        ['x', 'o', 'o'],
                                                        ['o', 'x', 'o'],
                                                        ['x', 'o', 'x']
                                                        
                                                        
                                                        ]) , 'x', 'should return x')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                       ['o','x', 'o'],
                                                       ['x', 'x', 'x'],
                                                       ['-', '-', '-']
                                                       ]), 'x', 'should return x'
                                                       )
        
        
        
    def test_these_should_win_for_o(self):
        
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard( [ ['o', 'x', 'o'], 
                                                          ['o', 'x', 'x'], 
                                                          ['o', 'o', 'x']]), 'o', "should return o")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                        ['x', 'o', '-'],
                                                        ['o', 'o', 'o'],
                                                        ['o', 'x', 'x']
                                                        
                                                        
                                                        ]) , 'o', 'should return o')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                       ['o','x', 'o'],
                                                       ['x', 'o', 'x'],
                                                       ['-', '-', 'o']
                                                       ]), 'o', 'should return o'
                                                       )
        


    def test_these_should_win_for_nobody(self):
        
                
        self.assertEqual(TicTacToe_Board.IsWinningBoard( [ ['x', 'x', '-'], 
                                                          ['o', '-', 'o'], 
                                                          ['o', '-', 'o']]), None, "should return None")
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                        ['-', '-', '-'],
                                                        ['-', '-', '-'],
                                                        ['x', 'o', 'x']
                                                        
                                                        
                                                        ]) , None, 'should return None')
        
        self.assertEqual(TicTacToe_Board.IsWinningBoard([
                                                       ['o','x', 'o'],
                                                       ['-', '-', 'x'],
                                                       ['-', 'o', 'o']
                                                       ]), None, 'should return None'
                                                       )
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()