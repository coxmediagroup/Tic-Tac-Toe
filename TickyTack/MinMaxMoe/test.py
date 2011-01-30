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



if __name__=="__main__":
    unittest.main()