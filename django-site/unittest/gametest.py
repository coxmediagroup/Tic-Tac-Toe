from apps.tictactoe.game import *
import unittest

class GameTest(unittest.TestCase):
    
    # verify that you can start the game
    def testInit(self):
        pass
    
    # verify that you can start a game as X and O
    def testAssignPlayer(self):
        pass
    
    # verify that getPlayer() returns the player that was assigned during init
    def testGetPlayer(self):
        pass
    
    # verify that makeMove() fails if it doesn't accept a 2-tuple
    def testMakeMove(self):
        pass
    
    # verify that makeMove() only accepts moves in-bounds