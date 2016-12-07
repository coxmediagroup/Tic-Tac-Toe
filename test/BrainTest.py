import unittest
from Brain import Brain
import Board
from TicTacToeExceptions import TokenPlacementException

class BrainTest(unittest.TestCase):


    def setUp(self):
        self.brain = Brain(Board.Board(player='O', computer='X'), 'X')

    def tearDown(self):
        del self.brain


    def test_evalMove(self):
        """Testing evaluateMove"""

        result = self.brain.evaluateMove(p='X')
        self.assertEqual(self.brain.best_move, 0)

    def test_evalMoveOneForWin(self):
        """Does Winning move return 1?"""

        data = ['X', 'O', 'X',
                'X', 'O', 'O',
                ' ', ' ', ' ']
        result = self.brain.evaluateMove(p='X', board=data)
        self.assertEqual(self.brain.best_move, 6)


    def test_evalMoveForDrawMove(self):
        """Does Drawing move return 0?"""

        data = ['X', 'O','X',
                'X', 'O','X',
                'O', ' ','O']
        result = self.brain.evaluateMove(p='X', board=data)
        self.assertEqual(result, 0)
        self.assertEqual(self.brain.best_move, 7)

    def test_evalMoveForBlock(self):
        """Can we throw a block?"""

        data = ['O', 'X', 'X' ,
                ' ', 'O', ' ' ,
                ' ', ' ', ' ']
        result = self.brain.evaluateMove(p='X', board=data)
        self.assertEqual(self.brain.best_move, 8)



