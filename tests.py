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


class TestComputer(unittest.TestCase):
    def setUp(self):
        self.game = Game('1')
        self.cpu = self.game.computer
        self.square = self.game.board.square

    def testStep1(self):
        '''
         O | O |
        ---+---+---
         O |   |
        ---+---+---
         X | X |
        '''
        self.square(0, 0).mark = 'O'
        self.square(0, 1).mark = 'O'
        self.square(0, 2).mark = 'X'
        self.square(1, 0).mark = 'O'
        self.square(1, 2).mark = 'X'
        sq20 = self.square(2, 0)

        self.assertIs(self.cpu.step1(self.game.board), sq20)
        self.assertFalse(self.cpu.step1(self.game.board))

    def testStep2(self):
        '''
         O | O |
        ---+---+---
         O |   |
        ---+---+---
         X | X |
        '''
        self.square(0, 0).mark = 'O'
        self.square(0, 1).mark = 'O'
        self.square(0, 2).mark = 'X'
        self.square(1, 0).mark = 'O'
        self.square(1, 2).mark = 'X'
        sq22 = self.square(2, 2)

        self.assertIs(self.cpu.step2(self.game.board), sq22)
        self.assertFalse(self.cpu.step2(self.game.board))

    def testStep3(self):
        '''
         O |   | X
        ---+---+---
           |   | O
        ---+---+---
           |   |
        '''
        self.square(0, 0).mark = 'O'
        self.square(2, 1).mark = 'O'
        self.square(2, 0).mark = 'X'
        sq01 = self.square(0, 1)
        sq11 = self.square(1, 1)

        self.assertIn(self.cpu.step3(self.game.board), [sq01, sq11])

        self.setUp()

        '''
         O |   |
        ---+---+---
           |   |
        ---+---+---
           |   | O
        '''
        self.square(0, 0).mark = 'O'
        self.square(2, 2).mark = 'O'

        sq20 = self.square(2, 0)
        sq02 = self.square(0, 2)

        self.assertIn(self.cpu.step3(self.game.board), [sq02, sq20])
        self.assertIn(self.cpu.step3(self.game.board), [sq02, sq20])
        self.assertFalse(self.cpu.step3(self.game.board))

    def testStep4(self):
        '''
         O |   |
        ---+---+---
           |   |
        ---+---+---
           |   |
        '''
        self.square(0, 0).mark = 'O'
        sq10 = self.square(1, 0)
        sq20 = self.square(2, 0)
        sq11 = self.square(1, 1)
        sq22 = self.square(2, 2)
        sq01 = self.square(0, 1)
        sq02 = self.square(0, 2)

        li = [sq10, sq20, sq11, sq22, sq01, sq02]
        self.assertIn(self.cpu.step4(self.game.board), li)

        sq10.mark = 'X'
        li = [sq01, sq02, sq11, sq22]
        self.assertIn(self.cpu.step4(self.game.board), li)

        sq22.mark = 'X'
        li = [sq01, sq02]
        self.assertIn(self.cpu.step4(self.game.board), li)

        self.setUp()

        '''
         X |   |
        ---+---+---
           |   |
        ---+---+---
         X |   |
        '''
        self.square(0, 0).mark = 'X'
        self.square(0, 2).mark = 'X'
        sq11 = self.square(1, 1)
        sq20 = self.square(2, 0)
        sq22 = self.square(2, 2)

        li = [sq11, sq20, sq22]
        self.assertIn(self.cpu.step4(self.game.board), li)

    def testStep5(self):
        sq11 = self.square(1, 1)

        self.assertIs(self.cpu.step5(self.game.board), sq11)
        self.assertFalse(self.cpu.step5(self.game.board))

    def testStep6(self):
        self.square(0, 0).mark = 'X'
        self.square(2, 0).mark = 'O'
        sq22 = self.square(2, 2)

        self.assertEqual(self.cpu.step6(self.game.board), sq22)

    def testStep7(self):
        self.square(0, 0).mark = 'X'
        self.square(2, 0).mark = 'O'
        sq22 = self.square(2, 2)
        sq02 = self.square(0, 2)

        self.assertIn(self.cpu.step7(self.game.board), [sq22, sq02])
        self.assertIn(self.cpu.step7(self.game.board), [sq22, sq02])
        for sq in self.game.board.corners():
            self.assertFalse(sq.empty())

    def testStep8(self):
        for sq in self.game.board.squares:
            sq.mark = 'X'
        sq10 = self.square(1, 0)
        sq22 = self.square(2, 2)
        sq10.mark = ' '
        sq22.mark = ' '

        self.assertIn(self.cpu.step8(self.game.board), [sq22, sq10])
        self.assertIn(self.cpu.step8(self.game.board), [sq22, sq10])
        self.assertEqual(self.game.board.unused(), [])


if __name__ == '__main__':
    unittest.main()
