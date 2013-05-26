#!/usr/bin/env python
import unittest
from tictactoe import *


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def get_squares(self, coords):
        '''Given a list of coordinate tuples, coords, return a list containing
        the square objects from board that are found at said coordinates.
        '''
        return [sq for sq in self.board.squares if (sq.x, sq.y) in coords]

    def test_square(self):
        sq21 = filter(lambda i: i.x == 2 and i.y == 1,
                      self.board.squares).pop()
        sq00 = filter(lambda i: i.x == 0 and i.y == 0,
                      self.board.squares).pop()

        self.assertEquals(self.board.square(2, 1), sq21)
        self.assertEquals(self.board.square(0, 0), sq00)
        with self.assertRaises(IndexError):
            self.board.square(3, 0)

    def test_used(self):
        '''
         X |   |
        ---+---+---
           | X | O
        ---+---+---
           |   |
        '''

        sq00 = self.board.square(0, 0)
        sq11 = self.board.square(1, 1)
        sq21 = self.board.square(2, 1)

        sq00.mark = 'X'
        sq21.mark = 'O'

        self.assertItemsEqual([sq21, sq00], self.board.used())

        sq11.mark = 'X'

        self.assertItemsEqual([sq00, sq11, sq21], self.board.used())

    def test_unused(self):
        '''
         X |   |
        ---+---+---
           | X | O
        ---+---+---
           |   |
        '''

        self.board.square(0, 0).mark = 'X'
        self.board.square(1, 1).mark = 'O'
        self.board.square(2, 1).mark = 'X'

        unused = [sq for sq in self.board.squares if sq.mark == ' ']
        self.assertItemsEqual(self.board.unused(), unused)

    def test_corners(self):
        corner_squares = self.get_squares([(0, 0), (2, 0), (0, 2), (2, 2)])
        self.assertItemsEqual(self.board.corners(), corner_squares)

    def test_winning_moves(self):
        '''
         X | O | X
        ---+---+---
         X |   |
        ---+---+---
           | O | X
        '''

        self.board.square(0, 0).mark = 'X'
        self.board.square(2, 2).mark = 'X'
        self.board.square(2, 0).mark = 'X'
        self.board.square(0, 1).mark = 'X'
        self.board.square(1, 0).mark = 'O'
        self.board.square(1, 2).mark = 'O'

        exs = self.get_squares([(0, 2), (1, 1), (2, 1)])
        ohs = self.get_squares([(1, 1)])

        self.assertItemsEqual(exs, self.board.winning_moves('X'))
        self.assertItemsEqual(ohs, self.board.winning_moves('O'))
        self.assertItemsEqual([], self.board.winning_moves('R'))

    def test_force_opponent(self):
        '''
           |   |
        ---+---+---
           |   |
        ---+---+---
         X |   | O
        '''

        self.board.square(0, 2).mark = 'X'
        self.board.square(2, 2).mark = 'O'

        forces = self.get_squares([(0, 0), (0, 1), (1, 1), (2, 0)])
        self.assertItemsEqual(self.board.force_opponent('X'), forces)

    def test_fork_available(self):
        '''
         O |   | X
        ---+---+---
           |   |
        ---+---+---
           | O |
        '''

        self.board.square(0, 0).mark = 'O'
        self.board.square(1, 2).mark = 'O'
        self.board.square(2, 0).mark = 'X'

        forks = self.get_squares([(1, 1), (0, 2), (2, 2)])
        self.assertItemsEqual(forks, self.board.fork_available('O'))
        self.assertItemsEqual([], self.board.fork_available('B'))

    def test_lines_of_sight(self):
        '''
         X |   | X
        ---+---+---
           |   | O
        ---+---+---
           |   |
        '''

        self.board.square(0, 0).mark = 'X'
        self.board.square(2, 0).mark = 'X'
        self.board.square(2, 1).mark = 'O'

        los = self.get_squares([(0, 0), (1, 0), (1, 1),
                                (0, 2), (2, 1), (2, 2)])
        sq20 = self.board.square(2, 0)
        self.assertItemsEqual(los, self.board.lines_of_sight(sq20))

        los = self.get_squares([(0, 1), (1, 1)])
        sq21 = self.board.square(2, 1)
        self.assertItemsEqual(los, self.board.lines_of_sight(sq21, solo=True))


class TestSquare(unittest.TestCase):
    def test_empty(self):
        sq = Square(0, 0)
        self.assertEquals(sq.empty(), True)
        sq.mark = 'X'
        self.assertEquals(sq.empty(), False)


if __name__ == '__main__':
    unittest.main()
