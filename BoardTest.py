import unittest
import random
import Board

from TicTacToeExceptions import *

class BoardTest(unittest.TestCase):
    
    
    def setUp(self):
        self.board = Board.Board()

    def tearDown(self):
        self.board = None




    def test_getPossibleMoves(self):
        """Can we get a list of possible remaining moves?"""
        expected = list()
        for i in range(9):
            ran = random.randint(8,9)
            token = ("x", None)[ran % 2] 
            self.board.addToken(token, i)
            if not token:
                expected.append(i)
        self.assertEqual(expected, self.board.getPossibleMoves())

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
        
