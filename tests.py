#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the unit tests.
""" 

import unittest
from engine import TTTEngine, TTTError, TTTMoveNode

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
        game.applyMove(3)
        game.applyMove(8)
        avail_moves = game.getValidMoves()
        self.assertTrue(3 not in avail_moves and 8 not in avail_moves)
        
    def testGetBestMove(self):
        # simulate an easy win opportunity and make sure the best move 
        # detected is the expected opportunity
        game = TTTEngine()
        game.applyMove(8)
        game.applyMove(5)
        game.applyMove(7)
        self.assertEqual(game.getBestMove(), 6)
        # also make sure all the test moves were rolled back
        self.assertEqual(game.moves, 3)
        
        # now test the typical X diagonal trick
        game = TTTEngine()
        game.applyMove(1)
        game.applyMove(4)
        game.applyMove(8)
        best_move = game.getBestMove()
        self.assertTrue(best_move != 6 and best_move != 2)
        
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
