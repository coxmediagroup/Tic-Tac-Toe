#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the unit tests.
""" 

import unittest
from engine import TTTEngine, TTTError

class UnitTests(unittest.TestCase):
    def setUp(self):
        pass
        
    def testInvalidMove(self):
        # tests to make sure any known invalid moves are caught
        game = TTTEngine()
        self.assertRaises(TTTError, game.applyMove, 0)
        self.assertRaises(TTTError, game.applyMove, -1)
        self.assertRaises(TTTError, game.applyMove, 'q')
        self.assertRaises(TTTError, game.applyMove, 'skjif32@)#)(@1')
        
    def testValidMove(self):
        # simulate a move; should not result in errors and move counter would
        # increment
        game = TTTEngine()
        game.applyMove(1)
        self.assertEqual(game.moves, 1)
        self.assertEqual(game.board[0], 'X')
        
    def testAvailableMoves(self):
        # simulate a move, then get the list of available moves; list should
        # not include the move submitted
        game = TTTEngine()
        game.applyMove(4)
        game.applyMove(9)
        avail_moves = game.getValidMoves()
        self.assertTrue(4 not in avail_moves and 9 not in avail_moves)
        
    def testXWinEndGame(self):
        # simulate a game where X wins
        pass
        
    def testOWinEndGame(self):
        # simulate a game where O wins
        pass
        
    def testStalemateEndGame(self):
        # simulate a game where a stalemate occurs
        pass
        
suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
unittest.TextTestRunner(verbosity=2).run(suite)
