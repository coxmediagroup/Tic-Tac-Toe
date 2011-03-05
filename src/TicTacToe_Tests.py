#
#Cox Media Group 'Tic-Tac-Toe' Coding Challenge
#Author: Samuel Aparo
#Created on Mar 5, 2011
#

import TicTacToe as ttt
import unittest


class Test(unittest.TestCase):

    #Setup: Instantiate a Board
    def setUp(self):
        self.gameBoard = ttt.Board()
        
    #Test reading and writing to a board class (valid case)
    def test_validReadAndWriteToGameBoard(self):
        self.gameBoard.updateBoard(0, 0, 1)
        mark = self.gameBoard.readBoard(0, 0)
        self.assertEqual(mark, 1)
    
    #Test reading and writing to a board class (invalid case)
    def test_invalidReadAndWriteToGameBoard(self):
        result = self.gameBoard.updateBoard(10, 1, 1)
        self.assertEqual(result, False)
        
    #Test board rendering after updating board in a few valid locations
    def test_renderBoard(self):
        self.gameBoard.updateBoard(0, 0, 1)
        self.gameBoard.updateBoard(1, 1, 2)
        self.gameBoard.updateBoard(2, 2, 1)
        output = self.gameBoard.renderBoard()
        self.assertEqual(output, 'X|_|_|\n_|O|_|\n_|_|X|\n')
        
if __name__ == "__main__":
    unittest.main()