import unittest
from tictactoe.board import Board
from tictactoe.ai import AI

class Test(unittest.TestCase):
    def testName(self):
        for x in range(1,10000):
            b=Board()
            randomAI=AI('x',AI.moveRandom)
            smartAI=AI('o',AI.moveAI)
            while not b.isFilled():
                randomAI.turn(b)
                if b.isWinner('o'):
                   print 'o is winner!\n' + str(b)
                   break
                smartAI.turn(b)
                if b.isWinner('x'):
                   print 'x is winner!\n' + str(b)
                   self.fail('X won with moves ' + str(b.moves))
            print 'Finished game ' + str(x) + '\n'
        pass
      
    def testDetectWin(self):
        b=Board()
        [b.mark(l,m) for l,m in ((2,'x'),(4,'x'))]
        smartAI=AI('x',AI.moveAI)
        self.assertEqual(smartAI.detectWin(b, 'x'), 6)
      
    def testDetectCorner(self):
        b=Board()
        [b.mark(l,m) for l,m in ((0,'x'),(4,'o'),(8,'x'))]
        smartAI=AI('o',AI.moveAI)
        self.assertEqual(smartAI.detectCornerManeuver(b), 1)
      
    def testDetectLine(self):
        b=Board()
        [b.mark(l,m) for l,m in ((0,'x'),(4,'o'),(8,'x'))]
        smartAI=AI('o',AI.moveAI)
        self.assertEqual(smartAI.moveAI(b), 1)

if __name__ == "__main__":
    unittest.main()