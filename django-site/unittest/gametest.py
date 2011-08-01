import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from apps.tictactoe.gameboard import GameBoard
import apps.tictactoe.game as game
import unittest

class GameTest(unittest.TestCase):
    
    # verify that the computer can never lose
    # recursively run through each possible play
    def testComputerNeverLoses(self):
        board = GameBoard()
        self.count = 0
        for cell in board.getEmptyCells():
            self._makeMove(board, cell)
        
        # computer makes first move
        for cell in board.getEmptyCells():
            board.makeMove(cell, game.ID_COMPUTER)
            for cell in board.getEmptyCells():
                self._makeMove(board, cell)
    
    # base case: win or full board
    def _makeMove(self, board, pmove):
        # move player
        board.makeMove(pmove, game.ID_PLAYER)
        self.assertEquals(False, board.checkForWin(0)) # player should never win
        
        if board.isFull():
            board.clear(pmove)
            return
        
        # move computer
        omove = game.getMove(board)
        board.makeMove(omove, game.ID_COMPUTER)
        
        if board.checkForWin(1) or board.isFull():
            board.clear(pmove)
            board.clear(omove)
            return
        
        for cell in board.getEmptyCells():
            self._makeMove(board, cell)
        
        board.clear(pmove)
        board.clear(omove)


if __name__ == '__main__':
    unittest.main()