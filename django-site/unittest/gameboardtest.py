import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(base_path)

from apps.tictactoe.gameboard import GameBoard, OutOfBoundsException, InvalidMoveException
import unittest

class BoundsTest(unittest.TestCase):
    
    # verify that all in-bound moves are acceptable
    def testInBounds(self):
        for playerId in range(2):
            b = GameBoard()
            for y in range(3):
                for x in range(3):
                    b.makeMove((x,y), playerId)
    
    # verify that any combination of invalid x or y coordinates raises exception
    def testOutBounds(self):
        for playerId in range(2):
            b = GameBoard()
            for y in (-3,-2,-1,4,5,6):
                for x in (-3,-2,-1,4,5,6):
                    self.assertRaises(OutOfBoundsException, b.makeMove, (x,y), playerId)
            
            b = GameBoard()
            for y in (-3,-2,-1,4,5,6):
                for x in range(3):
                    self.assertRaises(OutOfBoundsException, b.makeMove, (x,y), playerId)
                    
            b = GameBoard()
            for y in range(3):
                for x in (-3,-2,-1,4,5,6):
                    self.assertRaises(OutOfBoundsException, b.makeMove, (x,y), playerId)


class MoveTest(unittest.TestCase):
    
    # verify that all empty squares can be occupied through specified x,y coordinates
    def testMoveEmptyCellsByXY(self):
        for playerId in range(2):
            b = GameBoard()
            for y in range(3):
                for x in range(3):
                    b.makeMove((x,y), playerId)
    
    # verify that all empty squares can be occupied through all cell coordinates returned by getEmptyCells()
    def testMoveEmptyCellsByCell(self):
        for playerId in range(2):
            b = GameBoard()
            for cell in b.getEmptyCells():
                b.makeMove(cell, playerId)
    
    # verify that trying to move on an occupied square throws exception
    def testDoubleMove(self):
        for playerId in range(2):
            b = GameBoard()
            for y in range(3):
                for x in range(3):
                    b.makeMove((x,y), playerId)
                    self.assertRaises(InvalidMoveException, b.makeMove, (x,y), playerId)
    
    # verify that one player cannot make a move over another player
    def testPlayerOverPlayer(self):
        for playerId in range(2):
            b = GameBoard()
            for y in range(3):
                for x in range(3):
                    b.makeMove((x,y), playerId)
                    self.assertRaises(InvalidMoveException, b.makeMove, (x,y), range(2)[playerId-1])
    
    # verify player/turn ids that are not 0 or 1 raise an exception
    def testInvalidTurnException(self):
        for playerId in (-1,3,4):
            b = GameBoard()
            for y in range(3):
                for x in range(3):
                    self.assertRaises(InvalidMoveException, b.makeMove, (x,y), playerId)
        

class VacantTest(unittest.TestCase):
    
    # verify that getEmptyCells returns the number of all squares on the board
    def testInitialEmptyCellCount(self):
        b = GameBoard()
        self.assertEqual(len(b.getEmptyCells()), 9)
    
    # verify that getEmptyCells returns the correct number of empty cells after each move
    def testEmptyCellCount(self):
        for playerId in range(2):
            b = GameBoard()
            for cellCountShouldBe in (9,8,7,6,5,4,3,2,1,0):
                self.assertEquals(len(b.getEmptyCells()), cellCountShouldBe)
                if cellCountShouldBe > 0: b.makeMove(b.getEmptyCells()[0], playerId)


class WinTest(unittest.TestCase):
    
    # all possible wins (as a series of moves)
    wins = [
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)]
    ]
    
    # series of moves that do not lead to a win
    non_wins = [
        [(0,0),(1,0),(1,1)],
        [(0,1),(2,0),(2,1)],
        [(0,2),(1,0),(2,2)],
        
        [(1,1),(0,1),(0,2)],
        [(1,0),(1,1),(0,2)],
        [(2,0),(1,1),(2,2)],
        
        [(0,0),(1,1),(2,1)],
        [(1,2),(1,1),(2,0)]
    ]
    
    # verify that all default wins return true
    def testDefaultWins(self):
        for win in self.wins:
            for playerId in range(2):
                b = GameBoard()
                for move in win:
                    # move player
                    b.makeMove(move, playerId)
                    # move opponent
                    for cell in b.getEmptyCells():
                        if cell not in win:
                            b.makeMove(cell, range(2)[playerId-1])
                            break
                
                self.assertEqual(True, b.checkForWin(playerId))
                
        # test opponent wins
        for win in self.wins:
            for playerId in range(2):
                b = GameBoard()
                for move in win:
                    # move player
                    for cell in b.getEmptyCells():
                        if cell not in win:
                            b.makeMove(cell, playerId)
                            break
                    
                    # move opponenet
                    b.makeMove(move, range(2)[playerId-1])
                
                self.assertEqual(True, b.checkForWin(range(2)[playerId-1]))
    
    # verify that non-wins return false
    def testNonWins(self):
        for non_win in self.non_wins:
            for playerId in range(2):
                b = GameBoard()
                for move in non_win:
                    # move player
                    b.makeMove(move, playerId)
                    # move opponent
                    for cell in b.getEmptyCells():
                        if cell not in non_win:
                            b.makeMove(cell, range(2)[playerId-1])
                            break
                
                self.assertEqual(False, b.checkForWin(playerId))
        
        # test opponent non-wins
        for non_win in self.non_wins:
            for playerId in range(2):
                b = GameBoard()
                for move in non_win:
                    # move player
                    for cell in b.getEmptyCells():
                        if cell not in non_win:
                            b.makeMove(cell, playerId)
                            break
                    
                    # move opponent
                    b.makeMove(move, range(2)[playerId-1])
                
                self.assertEqual(False, b.checkForWin(range(2)[playerId-1]))


class EmptyAndFullTest(unittest.TestCase):
    
    def setUp(self):
        self.board = GameBoard()
    
    def tearDown(self):
        self.board = None
    
    # verify that an initial board is empty
    def testBoardEmpty(self):
        self.assertEquals(True, self.board.isEmpty())
    
    # verify that isFull() returns True when the board is full
    def testBoardFull0(self):
        for y in range(3):
            for x in range(3):
                self.board.makeMove((x,y), 0)
        
        self.assertEquals(True, self.board.isFull())
    
    # verify that isFull() returns True when the board is full
    def testBoardFull1(self):
        for y in range(3):
            for x in range(3):
                self.board.makeMove((x,y), 1)
        
        self.assertEquals(True, self.board.isFull())

if __name__ == '__main__':
    unittest.main()