import unittest

from app.ttt import *


class TicTacToeBoardTests(unittest.TestCase):
    # Testing done in binary as a second check to hex calculations in main class
    
    def test__init(self):
        # defaults
        ttt = TicTacToeBoard()
        for attr in ('board', 'turn', 'player_wins', 'player_losses', 'ties'):
            self.assertEquals(0, getattr(ttt, attr))
    
    def test__convert_move(self):
        ttt = TicTacToeBoard()
        # testing for O
        for move, expected in ((0, 0b000000000000000010), (1, 0b000000000000001000),
                               (2, 0b000000000000100000), (3, 0b000000000010000000),
                               (4, 0b000000001000000000), (5, 0b000000100000000000),
                               (6, 0b000010000000000000), (7, 0b001000000000000000),
                               (8, 0b100000000000000000)):
            self.assertEquals(expected, ttt._convert_move(move))
        
        # testing for X
        ttt.turn = 1
        for move, expected in ((0, 0b000000000000000011), (1, 0b000000000000001100),
                               (2, 0b000000000000110000), (3, 0b000000000011000000),
                               (4, 0b000000001100000000), (5, 0b000000110000000000),
                               (6, 0b000011000000000000), (7, 0b001100000000000000),
                               (8, 0b110000000000000000)):
            self.assertEquals(expected, ttt._convert_move(move))
            
        # should return None for integers 0 <= move <= 8
        for move in (-2, -1, 9, 10):
            self.assertIsNone(ttt._convert_move(move))
        
        # should return None for moves that can't be converted to integers
        for move in ('a', None, {}):
            self.assertIsNone(ttt._convert_move(move))
    
    def test__is_valid(self):
        self.assertTrue(False, "Test not implemented")
    
    def test__set_turn(self):
        ttt = TicTacToeBoard()
        self.assertEquals(0, ttt.turn)
        
        # should alternate between 1 and 0
        for turn in (1, 0, 1, 0, 1, 0, 1, 0):
            ttt._set_turn()
            self.assertEquals(turn, ttt.turn)
    
    def test_apply_move(self):
        ttt = TicTacToeBoard()
        self.assertEquals(0, ttt.board)
        self.assertEquals(0, ttt.turn)
        
        # empty board should always apply
        self.assertTrue(ttt.apply_move(3))
        self.assertEquals(0b000000000010000000, ttt.board)
        
        # some intermediate test cases
        ttt.turn = 1
        self.assertTrue(ttt.apply_move(5))
        self.assertEquals(0b000000110010000000, ttt.board)
        
        ttt.turn = 0
        self.assertFalse(ttt.apply_move(5))
        self.assertEquals(0b000000110010000000, ttt.board)
        self.assertTrue(ttt.apply_move(8))
        self.assertEquals(0b100000110010000000, ttt.board)
        
        # full board should never apply
        ttt.board = 0b101011101110101111
        for turn in (0, 1):
            ttt.turn = turn
            for move in range(0, 9):
                self.assertFalse(ttt.apply_move(move))
                self.assertEquals(0b101011101110101111, ttt.board)
    
    def test_is_computer_turn(self):
        ttt = TicTacToeBoard()
        for turn in (0, 1):
            ttt.turn = turn
            self.assertEquals(bool(turn), ttt.is_computer_turn())

