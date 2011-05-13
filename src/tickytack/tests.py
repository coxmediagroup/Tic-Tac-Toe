import unittest

from tickytack.engines import random_choice
from tickytack.engines import ROWS
from tickytack.views import new_board


NOT_WINS = [['','','o', 
             'x', 'o', 'x', 
             '', '', 'x'],
            ['x', '', '',
             'x', '', '',
             'o', '', '',],
            ['', '', 'o',
             '', 'x', '',
             'x', '', '',],
            ['x', '', '',
             '', 'x', '',
             '', '', 'o',],]

WINS = [['x', 'x', 'x',
         '', '', 'o',
         '', 'o', '',],
        ['x', '', '',
         'x', 'o', '',
         'x', 'o', '',],
        ['x', '', 'o',
         '', 'x', 'o',
         '', '', 'x',],
        ['', 'o', 'x',
         '', 'x', '',
         'x', 'o', '',],]

class TestRandomChoiceEngine(unittest.TestCase):
    
    def setUp(self):
        self.board = new_board()
        self.engine = random_choice
    
    def test_is_win(self):
        # an empty board cannot be a win
        self.assertFalse(self.engine.is_win(self.board))
        for board in NOT_WINS:
            print board
            self.assertFalse(self.engine.is_win(board))
        for board in WINS:
            print board
            self.assertTrue(self.engine.is_win(board))