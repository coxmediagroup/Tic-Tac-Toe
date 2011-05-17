"""
Tests for basic board operations.
"""

import unittest
import ttt

class TestBoardBasic(unittest.TestCase):
    def make_board(self, board):
        """(str): Board

        Assembles a board from a 9-character string containing 
        '-', 'X', and 'O'.
        """
        assert len(board) == 9
        b = ttt.Board()
        for cell, ch in enumerate(board):
            if ch in (ttt.PLAYER_1, ttt.PLAYER_2):
                b.record(cell, ch)
        return b

    def test_blank(self):
        b = self.make_board('---------')
        for i in range(9):
            self.assertTrue(b.is_cell_blank(i))
            b.record(i, ttt.PLAYER_1)
            self.assertFalse(b.is_cell_blank(i))

if __name__ == '__main__':
    unittest.main()
