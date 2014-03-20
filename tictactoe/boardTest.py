import unittest
from tictactoe.board import Board

class Test(unittest.TestCase):
    def testWin(self):
        b=Board()
        [b.mark(l,m) for l,m in ((2,'x'),(4,'x'))]
        self.assertFalse(b.isWinner('x'))
        b.mark(6, 'x')
        print b
        self.assertTrue(b.isWinner('x'))
        
    def testEmptyExcept(self):
        b=Board()
        [b.mark(l,m) for l,m in ((2,'x'),(4,'x'))]
        self.assertTrue(b.isEmptyExcept((2,4)))

if __name__ == "__main__":
    unittest.main()