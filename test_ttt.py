"""
Tests for basic board operations.
"""

import unittest
import StringIO
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

    def test_copy(self):
        b = self.make_board('---------')
        copy = b.copy()
        # Require the two internal lists have the same contents...
        self.assertEquals(b._board, copy._board)
        # ...but that they are different objects.
        self.assertTrue(b._board is not copy._board)

    def test_empty(self):
        b = self.make_board('---------')
        self.assertTrue(b.is_empty())
        b = self.make_board('X--------')
        self.assertFalse(b.is_empty())
        b = self.make_board('XOXOXOXOX')
        self.assertFalse(b.is_empty())

    def test_full(self):
        b = self.make_board('---------')
        self.assertFalse(b.is_full())
        b = self.make_board('XOXOXOXO-')
        self.assertFalse(b.is_full())
        b = self.make_board('XOXOXOXOX')
        self.assertTrue(b.is_full())
            
    def test_output(self):
        # This test will exercise the output() method for several cases
        # and captures the output, but only verifies that the method
        # doesn't raise an exception.
        for board in ('---------', 'XOXOXOOXO'):
            b = self.make_board(board)
            out = StringIO.StringIO()
            b.output(out)
            ##print out.getvalue()
                
    def test_winner(self):
        for (expected, board) in [
            (None, '---------'), # Empty board
            (None, 'XOXOXOOXO'), # Randomly full board
            # Horizontals
            ('X', 'XXX------'),
            ('X', '---XXX---'),
            ('X', '------XXX'),
            # Verticals
            ('O', 'O--O--O--'),
            ('O', '-O--O--O-'),
            ('O', '--O--O--O'),
            # Diagonals
            ('O', 'O---O---O'),
            ('X', '--X-X-X--'),
            ]:
            b = self.make_board(board)
            self.assertEquals(b.get_winner(), expected)

    def test_minimax_first_move(self):
        # Test that the search will pick the middle square on an empty board.
        b = self.make_board('---------')
        self.assertEquals(b.find_move(ttt.PLAYER_1), 4)

    def test_minimax_first_move(self):
        # Test that the search will pick the middle square on an empty board.
        b = self.make_board('---------')
        self.assertEquals(b.find_move(ttt.PLAYER_1), 4)

    def test_minimax_pick_winner(self):
        # Test that the search will notice a winning opportunity for 'X'
        # by taking cell 3.
        b = self.make_board('XX--O-O--')
        self.assertEquals(b.find_move(ttt.PLAYER_1), 2)

    def test_minimax_prefer_corner(self):
        # Check that the search will prefer a corner square.
        b = self.make_board('----X----')
        self.assertIn(b.find_move(ttt.PLAYER_2), 
                      [ttt.UL_SQUARE, ttt.UR_SQUARE,
                       ttt.LL_SQUARE, ttt.LR_SQUARE])

    def test_minimax_prevent_loss(self):
        # Test that the minimax search will notice a loss for 'X' when
        # 'O' takes cell 7 on the next move, and take that cell to
        # prevent it.
        b = self.make_board('XXO-O----')
        self.assertEquals(b.find_move(ttt.PLAYER_1), 6)

if __name__ == '__main__':
    unittest.main()
