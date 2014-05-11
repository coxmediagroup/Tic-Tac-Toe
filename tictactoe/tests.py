from django.test import SimpleTestCase

from .models import Board


class BoardTest(SimpleTestCase):
    def test_new_game(self):
        b = Board()
        expected = (
            ' | | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(0, b.state())
        self.assertEqual(Board.MARK_X, b.next_mark())
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertFalse(b.winner())

    def test_one_move(self):
        b = Board(state=1)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertEqual(Board.MARK_O, b.next_mark())
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertFalse(b.winner())

    def test_row1_winner(self):
        b = Board(state=14755)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            ' |O| \n'
            '-+-+-\n'
            'O| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())
        self.assertEqual(Board.BLANK, b.next_mark())
        self.assertEqual([], b.next_moves())

    def test_row2_winner(self):
        b = Board(state=9453)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|O|O\n'
            '-+-+-\n'
            ' |X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_row3_winner(self):
        b = Board(state=9695)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            'X|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_col1_winner(self):
        b = Board(state=10343)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_col2_winner(self):
        b = Board(state=3783)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X| ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_col3_winner(self):
        b = Board(state=14439)
        expected = (
            ' |X|O\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_rising_slash_winner(self):
        b = Board(state=14427)
        expected = (
            ' | |X\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_falling_slash_winner(self):
        b = Board(state=14267)
        expected = (
            'O| |X\n'
            '-+-+-\n'
            ' |O|X\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_two_way_winner(self):
        self.assertRaises(ValueError, Board, state=715)
        b = Board(state=18859)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            'O|X|O\n'
            '-+-+-\n'
            'X|O|O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_two_winners_invalid(self):
        self.assertRaises(ValueError, Board, state=715)
        # This corresponds to this board:
        # X|X|X #
        # -+-+- #
        # O|O|O #
        # -+-+- #
        #  | |  #

    def test_invalid_large_state(self):
        self.assertRaises(ValueError, Board, state=pow(3, 9))

    def test_invalid_O_first(self):
        self.assertRaises(ValueError, Board, state=2)

    def test_invalid_too_many_X(self):
        self.assertRaises(ValueError, Board, state=4)

    def test_valid_move(self):
        b = Board()
        b.move(0)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertFalse(b.winner())

    def test_invalid_move(self):
        b = Board(state=1)
        self.assertRaises(ValueError, b.move, 0)
