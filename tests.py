#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the unit tests.
""" 

import unittest
from engine import TTTEngine, TTTError, TTTMoveNode, TTTEndGame

class UnitTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def testInvalidMove(self):
        # tests to make sure any known invalid moves are caught
        game = TTTEngine()
        
        for i in ( 9, -1, 'q', 'skjif32@)#)(@1' ):
            self.assertRaises(TTTError, game.applyMove, i)
        
    def testValidMove(self):
        # simulate a move; should not result in errors and move counter would
        # increment
        game = TTTEngine()
        game.applyMove(4)
        self.assertEqual(game.moves, 1)
        self.assertEqual(game.board[4], 'X')
        
    def testAvailableMoves(self):
        # simulate a move, then get the list of available moves; list should
        # not include the move submitted
        game = TTTEngine()
        
        for i in (0,4,1,8):
            game.applyMove(i)
            avail_moves = game.getValidMoves()
            self.assertTrue( i not in avail_moves )
    
    def testGetBestMove(self):
        # Simulate an easy win opportunity for X and make sure the best move 
        # detected is the expected opportunity (look ahead 1 move).
        # Note "best" move is just whatever move prevents the player from winning
        # and the AI won't neccessarily see moves that make it win instantly.
        game = TTTEngine()
        game.applyMove(0)
        game.applyMove(4)
        game.applyMove(1)
        self.assertEqual(game.getBestMove(), 2)
        # also make sure all the test moves were rolled back
        self.assertEqual(game.moves, 3)
        
        # a little more complicated (look ahead 2 moves).
        game = TTTEngine()
        game.applyMove(4)
        game.applyMove(0)
        game.applyMove(8)
        best = game.getBestMove()
        self.assertTrue(best in (2, 6))
        
        game = TTTEngine()
        game.applyMove(6)
        game.applyMove(4)
        game.applyMove(0)
        best = game.getBestMove()
        self.assertTrue(best in (1, 3, 5, 7))
        
        # another edge case uncovered by the random number gen when it wouldn't win.
        game = TTTEngine()
        game.applyMove(0)
        game.applyMove( game.getBestMove() )
        game.applyMove(8)
        game.applyMove( game.getBestMove() )
        game.applyMove(6)
        self.assertEqual( game.getBestMove(), 3 )
        
    
    def testXWinEndGame(self):
        # simulate a game where X wins
        game = TTTEngine()
        
        for i in ( 0, 3, 1, 4 ):
            game.applyMove(i)
            
        try:
            game.applyMove(2)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'You won!' )
        
    def testOWinEndGame(self):
        # simulate a game where O wins
        game = TTTEngine()
        
        for i in ( 3, 0, 5, 4, 7 ):
            game.applyMove( i )
            
        try:
            game.applyMove(8)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'I won!' )
            
        
    def testStalemateEndGame(self):
        # simulate a game where a stalemate occurs
        game = TTTEngine()
        
        for i in ( 4, 0, 1, 7, 6, 2, 5, 3 ):
            game.applyMove(i)
            
        try:
            game.applyMove(8)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'Stalemate!' )
        
    # Removed the random generator because it would make illegal plays like not making three in a row
    # when it could, and then the AI logic would break down.
    
suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
unittest.TextTestRunner(verbosity=2).run(suite)

