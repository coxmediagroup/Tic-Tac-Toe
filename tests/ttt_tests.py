import unittest

from app.ttt import *


class TicTacToeBoardTests(unittest.TestCase):
    def test__init(self):
        # defaults
        ttt = TicTacToeBoard()
        for attr in ('board', 'turn', 'player_wins', 'player_losses', 'ties'):
            self.assertEquals(0, getattr(ttt, attr))
    
    def test_is_computer_turn(self):
        pass