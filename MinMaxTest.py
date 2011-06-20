import unittest
from Brain import Brain
from pprint import pprint as pp

class MinMaxTest(unittest.TestCase):
    
    
    def setUp(self):
        self.brain = Brain()
        
    def tearDown(self):
        self.brain = None


    def test_evalMove(self):
        """Testing evaluateMove"""

        r = self.brain.evaluateMove(1,'x')
        self.assertEqual(r, 0)

    def test_evalMoveOneForWin(self):
        """Does Winning move return 1?"""

        data = ['x', 'o','x' ,'x' ,'o' ,'o' ,None, None, None]
        r = self.brain.evaluateMove(6,'x', board=data)
        self.assertEqual(r, 1)


    def test_evalMoveForDrawMove(self):
        """Does Drawing move return 0?"""

        data = ['x', 'o','x' ,'x' ,'o' ,'o' ,None, None, None]
        r = self.brain.evaluateMove(7,'x', board=data)
        self.assertEqual(r, 0)
        
    def test_evalMoveForBadMove(self):
        """Does Losing move return -1?"""

        data = ['x', 'o','x' ,'x' ,'o' ,'o' ,None, None, None]
        r = self.brain.evaluateMove(8,'x', board=data)
        self.assertEqual(r, -1)
