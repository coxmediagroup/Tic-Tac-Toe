#!/usr/bin/env python

import unittest
import board


class BoardTests(unittest.TestCase):

    def test_check_squares_valid(self):
        b = board.Board(9)
        for i in xrange(0, 9):
            b._is_valid_square(i)

    def test_check_squares_invalid(self):
        b = board.Board(9)
        self.assertRaises(board.BoardError, b._is_valid_square, -1)
        self.assertRaises(board.BoardError, b._is_valid_square, 9)

    def test_is_full(self):
        b = board.Board(9)
        for i in xrange(0, 8):
            b.place(i, "X")
            self.assertFalse(b.is_full())

        b.place(8, "X")
        self.assertTrue(b.is_full())

    def test_square_free(self):
        b = board.Board(9)
        for i in xrange(0, 9):
            self.assertTrue(b.square_free(i))
            b.place(i, "X")
            self.assertFalse(b.square_free(i))

    def test_place(self):
        b = board.Board(9)
        for i in xrange(0, 9):
            b.place(i, "X")

    def test_place_error_full(self):
        b = board.Board(9)
        for i in xrange(0, 9):
            b.place(i, "X")

        self.assertRaises(board.BoardError, b.place, 0, "X")

    def test_place_error_taken(self):
        def check(square):
            b = board.Board(9)
            b.place(square, "X")
            self.assertRaises(board.BoardError, b.place, square, "X")

        for i in xrange(0, 9):
            check(i)


if __name__ == "__main__":
    unittest.main()
