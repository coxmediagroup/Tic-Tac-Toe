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



if __name__=="__main__":
    unittest.main()