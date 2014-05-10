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

    def test_two_moves(self):
        b = Board(state=5)
        expected = (
            'O|X| \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(5, b.state())
        self.assertEqual(Board.MARK_X, b.next_mark())
        self.assertEqual([2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertFalse(b.winner())

    def test_invalid_large_state(self):
        self.assertRaises(ValueError, Board, state=1000000)

    def test_invalid_O_first(self):
        self.assertRaises(ValueError, Board, state=2)

    def test_invalid_too_many_X(self):
        self.assertRaises(ValueError, Board, state=4)
        self.assertRaises(ValueError, Board, state=2)
