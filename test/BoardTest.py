import unittest
import random
import Board
import Brain
import mock

from TicTacToeExceptions import *

class BoardTest(unittest.TestCase):


    def setUp(self):
        self.board = Board.Board()

    def tearDown(self):
        self.board = None

    def test_is_winner_draw(self):
        """Everybody wins! Everyone gets a ribbon! and some chicken wings"""
        self.board.judge.evalGame = mock.Mock(return_value=[None, 'done'])
        result = self.board.isWinner()
        self.assertEqual(result, 'draw')

    def test_is_winner_not_over(self):
        """We are still playing"""
        self.board.judge.evalGame = mock.Mock(return_value=[None, None])
        result = self.board.isWinner()
        self.assertEqual(result, False)

    def test_is_winner(self):
        """We gotta winner! Mr. X"""
        self.board.judge.evalGame = mock.Mock(return_value=['X', 'done'])
        result = self.board.isWinner()
        self.assertEqual(result, 'win')

    def test_make_computer_move(self):
        """Can we have the computer make a move?"""
        self.board.computer_token = 'X'
        brain = Brain.Brain(Board.Board(), self.board.computer_token)
        self.board.makeComputerMove(brain)
        self.assertEqual(self.board.tokens[4], 'X')

    def test_get_player_move(self):
        """Can we get our player move"""
        self.board._raw_input = mock.Mock(return_value=1)
        self.board.firstMove = mock.Mock(return_value='player')
        self.board.player_token = 'X'
        self.board.getPlayerMove()
        self.assertEqual(self.board.tokens[0], 'X')


    def test_draw_board(self):
        """Lets draw the board!!"""
        expected = '\n\n | | \n'
        expected += '_____\n'
        expected += ' | | \n'
        expected += '_____\n'
        expected += ' | | \n\n'


        result = self.board.drawBoard()
        self.assertEqual(result, expected)


    @mock.patch('Board.random')
    def test_first_move(self, mock_random):
        """Can we randomly select who goes first?"""
        mock_random.randint.return_value = 0
        expected = 'player'
        result = self.board.firstMove()
        self.assertEqual(result, expected)

    def test_input_letter(self):
        """Does our letter get input correctly?"""
        self.board._raw_input = mock.Mock(return_value='X')
        self.assertIsNone(self.board.player_token)
        self.assertIsNone(self.board.computer_token)
        self.board.inputPlayerLetter()
        self.assertEqual(self.board.player_token, 'X')
        self.assertEqual(self.board.computer_token, 'O')

    def test_getPossibleMoves(self):
        """Can we get a list of possible remaining moves?"""
        expected = list()
        for i in range(9):
            ran = random.randint(8,9)
            token = ("X", ' ')[ran % 2]
            if token != 'X':
                expected.append(i)
            else:
                self.board.addToken(token, i)
        result = self.board.getPossibleMoves()
        self.assertEqual(expected, result)

    def test_addToken(self):
        """Can we add a token to a known empty space?"""
        local_board = []
        for i in range(9):
            ran = random.randint(8,9)
            token = ("x", "o")[ran % 2]
            self.board.addToken(token, i)
            local_board.append(token)
        self.assertEqual(local_board, self.board.getBoard())

    def test_upperIndexRaisesException(self):
        """Does an index higher than expected raise a TokenPlacementException?"""
        self.assertRaises(TokenPlacementException, self.board.addToken, "x", 9)

    def test_lowerIndexRaisesException(self):
        """Does an index lower than expected raise a TokenPlacementException?"""
        self.assertRaises(TokenPlacementException, self.board.addToken, "x", -1)

    def test_placeTokenInFilledSpot(self):
        """Place a token in a filled spot prevented?"""
        self.board.addToken("x", 0)
        self.assertRaises(TokenPlacementException, self.board.addToken, "x", 0)
