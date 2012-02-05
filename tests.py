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
        self.assertRaises(TTTError, game.applyMove, 9)
        self.assertRaises(TTTError, game.applyMove, -1)
        self.assertRaises(TTTError, game.applyMove, 'q')
        self.assertRaises(TTTError, game.applyMove, 'skjif32@)#)(@1')
        
    def testValidMove(self):
        # simulate a move; should not result in errors and move counter would
        # increment
        game = TTTEngine()
        game.applyMove(0)
        self.assertEqual(game.moves, 1)
        self.assertEqual(game.board[0], 'X')
        
    def testAvailableMoves(self):
        # simulate a move, then get the list of available moves; list should
        # not include the move submitted
        game = TTTEngine()
        game.applyMove(0)
        game.applyMove(4)
        game.applyMove(1)
        game.applyMove(8)
        avail_moves = game.getValidMoves()
        self.assertTrue(0 not in avail_moves and 1 not in avail_moves and \
            4 not in avail_moves and 8 not in avail_moves)
    
    def testGetBestMove(self):
        # simulate an easy win opportunity and make sure the best move 
        # detected is the expected opportunity (look ahead 1 move)
        game = TTTEngine()
        game.applyMove(0)
        game.applyMove(4)
        game.applyMove(1)
        self.assertEqual(game.getBestMove(), 2)
        # also make sure all the test moves were rolled back
        self.assertEqual(game.moves, 3)
        
        # a little more complicated (look ahead 2 moves)
        game = TTTEngine()
        game.applyMove(4)
        game.applyMove(0)
        game.applyMove(8)
        self.assertEqual(game.getBestMove(), 2)
        
        game = TTTEngine()
        game.applyMove(6)
        game.applyMove(4)
        game.applyMove(0)
        self.assertEqual(game.getBestMove(), 3)
        
        # simulate a win that takes priority over blocking
        game = TTTEngine()
        game.applyMove(5)
        game.applyMove(4)
        game.applyMove(3)
        game.applyMove(7)
        game.applyMove(0)
        self.assertEqual( game.getBestMove(), 1)
    
    def testXWinEndGame(self):
        # simulate a game where X wins
        game = TTTEngine()
        game.applyMove(0)
        game.applyMove(3)
        game.applyMove(1)
        game.applyMove(4)
        try:
            game.applyMove(2)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'You won!' )
        
    def testOWinEndGame(self):
        # simulate a game where O wins
        game = TTTEngine()
        game.applyMove(3)
        game.applyMove(0)
        game.applyMove(5)
        game.applyMove(4)
        game.applyMove(7)
        try:
            game.applyMove(8)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'I won!' )
            
        
    def testStalemateEndGame(self):
        # simulate a game where a stalemate occurs
        game = TTTEngine()
        game.applyMove(4)
        game.applyMove(0)
        game.applyMove(1)
        game.applyMove(7)
        game.applyMove(6)
        game.applyMove(2)
        game.applyMove(5)
        game.applyMove(3)
        try:
            game.applyMove(8)
        except TTTEndGame as e:
            self.assertEqual( str(e), 'Stalemate!' )
    
suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
unittest.TextTestRunner(verbosity=2).run(suite)

