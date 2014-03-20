import unittest
import Judge
import Board

class JudgeTest(unittest.TestCase):


    def setUp(self):

        self.winners = [['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
                       ,[' ', ' ', ' ', 'X', 'X', 'X', ' ', ' ', ' ']
                       ,[' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X']
                       ,['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']
                       ,[' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X', ' ']
                       ,[' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X']
                       ,['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
                       ,[' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ']]


    def test_Winners(self):
        """Do all winning boards evaluate as a winner?"""

        for w in self.winners:
            board = Board.Board()
            board.tokens = w
            judge = Judge.Judge(board)
            result = judge.isWinner()
            self.assertEqual(result, "X")

    def test_notWinnerNotDone(self):
        """Do we get the correct response for an unfinished game?"""
        tokens = ['X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        board = Board.Board()
        board.tokens = tokens
        judge = Judge.Judge(board)
        result = judge.isWinner()
        self.assertEqual(result, None)

    def test_draw(self):
        """Do we get the correct response for a draw game?"""

        tokens = ['X', 'O', 'X', 'X', 'O', 'X', 'O', 'X', 'O']
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
        self.assertEqual(result, [None, None])

    def test_evalGameWinner(self):
        """Is the game Over with a winner?"""
        board = Board.Board()
        board.tokens = ['X', 'X', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        judge = Judge.Judge(board)
        result = judge.evalGame()
        self.assertEqual(result, ['X','done'])

    def test_evalGameDraw(self):
        """Is the game Over with a draw?"""
        board = Board.Board()
        board.tokens = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        judge = Judge.Judge(board)
        result = judge.evalGame()
        self.assertEqual(result, [None,'done'])
