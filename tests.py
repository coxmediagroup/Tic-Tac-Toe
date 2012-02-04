#!/usr/bin/python
# Bernhardt, Russell
# russell.bernhardt@gmail.com

""" This module contains all the unit tests.
""" 

import unittest

class UnitTests(unittest.TestCase):
    def setUp(self):
        pass
        
    def testInvalidMove(self):
        # tests to make sure a known invalid moves are caught
        pass
        
    def testValidMove(self):
        # simulate a move; should not result in errors and move counter would
        # increment
        pass
        
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
