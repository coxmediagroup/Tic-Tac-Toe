import unittest
from MinMaxMoe.tictactoe import *


class GridTest(unittest.TestCase):

    def test_grid(self):

        g = Grid()
        self.assertEquals('_ _ _\n_ _ _\n_ _ _', str(g))
        self.assertEquals('_', g.A1)
        g.A1 = X
        g.B2 = O
        self.assertEquals('X _ _\n_ O _\n_ _ _', str(g))



class TicTacToeTest(unittest.TestCase):

    def test_moves(self):

        t1 = TicTacToe()
        self.assertEquals('start', t1.path)
        self.assertEquals(X, t1.toPlay)
        self.assertEquals(('XA1', 'XA2', 'XA3',
                           'XB1', 'XB2', 'XB3',
                           'XC1', 'XC2', 'XC3'), t1.moves)

        # move to the center:
        t2 = t1.XB2
        self.assertEquals('start.XB2', t2.path)
        self.assertEquals(O, t2.toPlay)
        self.assertEquals('_ _ _\n_ X _\n_ _ _', str(t2))
        self.assertEquals('_ _ _\n_ _ _\n_ _ _', str(t1)) # shouldn't change!
        self.assertEquals(('OA1', 'OA2', 'OA3',
                           'OB1',        'OB3',
                           'OC1', 'OC2', 'OC3'), t2.moves)



    def test_winner(self):

        g = TicTacToe().XB2.OA1.XA2.OB1
        self.assertEquals('O O _\nX X _\n_ _ _', str(g))
        self.failIf(g.isOver, "not quite yet")
        self.assertEquals(kUnknown, g.winner)

        g = g.XC2
        self.assertEquals('O O _\nX X X\n_ _ _', str(g))
        self.failUnless(g.isOver, "should be over because X won")
        self.assertEquals(X, g.winner)


    def test_tied(self):

        g = TicTacToe().XB2.OA1.XA2.OC2.XC1.OA3.XB3.OB1.XC3
        self.assertEquals('O O X\nX X O\nO X X', str(g))
        self.failUnless(g.isOver, "should be over because grid is full")
        self.assertEquals(kTie, g.winner)


if __name__=="__main__":
    unittest.main()