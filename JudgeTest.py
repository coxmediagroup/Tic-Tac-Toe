import unittest
import Judge
import Board

class JudgeTest(unittest.TestCase):
    
    
    def setUp(self):

        self.winners = [['x', 'x', 'x', None, None, None, None, None, None]
                       ,[None, None, None, 'x', 'x', 'x', None, None, None]
                       ,[None, None, None, None, None, None, 'x', 'x', 'x']
                       ,['x', None, None, 'x', None, None, 'x', None, None]
                       ,[None, 'x', None, None, 'x', None, None, 'x', None]
                       ,[None, None, 'x', None, None, 'x', None, None, 'x']
                       ,['x', None, None, None, 'x', None, None, None, 'x']
                       ,[None, None, 'x', None, 'x', None, 'x', None, None]]


    def test_Winners(self):
        """Do all winning boards evaluate as a winner?"""

        for w in self.winners:
            board = Board.Board()
            board.tokens = w
            judge = Judge.Judge(board)
            result = judge.isWinner()
            self.assertEqual(result, "x")

    def test_notWinnerNotDone(self):
        """Do we get the correct response for an unfinished game?"""
        tokens = ['x', 'o', None, None, None, None, None, None, None]
        board = Board.Board()
        board.tokens = tokens
        judge = Judge.Judge(board)
        result = judge.isWinner()
        self.assertEqual(result, None)

    def test_draw(self):
        """Do we get the correct response for a draw game?"""
        tokens = ['x', 'o', 'x', 'o', 'x', 'o', 'o', 'x', 'o']
        board = Board.Board()
        board.tokens = tokens
        judge = Judge.Judge(board)
        result = judge.isWinner()
        self.assertEqual(result, None)

    def test_evalGame(self):
        """Is the game still going?"""
        board = Board.Board()
        judge = Judge.Judge(board)
        result = judge.evalGame()
        self.assertEqual(result, None)

    def test_evalGameWinner(self):
        """Is the game Over with a winner?"""
        board = Board.Board()
        board.tokens = ['x', 'x', 'x', 'o', 'x', 'o', 'o', 'x', 'o']
        judge = Judge.Judge(board)
        result = judge.evalGame()
        self.assertEqual(result, ['x','done'])

    def test_evalGameDraw(self):
        """Is the game Over with a draw?"""
        board = Board.Board()
        board.tokens = ['x', 'o', 'x', 'o', 'x', 'o', 'o', 'x', 'o']
        judge = Judge.Judge(board)
        result = judge.evalGame()
        self.assertEqual(result, [None,'done'])
