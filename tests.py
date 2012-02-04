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
