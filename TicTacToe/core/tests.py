"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
from core.game import Game
from core.const import PLAYERS, WIN_VECTORS


class TicTacToeTest(unittest.TestCase):

    def setUp(self):
        self.board = Game()

    def tearDown(self):
        pass

    def test_001(self):
        """
        Test the available move checker
        """
        moves = self.board.available()
        self.assertTrue(len(moves) == 9, 'Not all moves are available')
        self.assertTrue(moves == [0, 1, 2, 3, 4, 5, 6, 7, 8], 'Available moves do not match')

    def test_002(self):
        """
        Test position setter
        """
        self.board.take('machine', 4)  # Machine takes center position
        moves = self.board.available()
        self.assertTrue(len(moves) == 8, 'Position not taken')
        self.assertTrue(moves == [0, 1, 2, 3, 5, 6, 7, 8], 'Available moves do not match')

    def test_003(self):
        """
        Test win detection
        """
        self.board.take('machine', 1)
        # At this point we shoulnd't have a winner yet
        self.assertFalse(self.board.win('machine'), 'We have a winner')
        self.board.take('machine', 7)
        # Now the machine player should have won
        self.assertTrue(self.board.win('machine'), '{0} is not the winner'.format(PLAYERS['machine']))
        self.assertTrue(self.board.win('machine') == (1, 4, 7), 'Unexpected winning vector')

    def test_004(self):
        """
        Test win detection
        """
        self.board._clear('machine', 1)
        # Now the machine player should have a winning move available
        self.assertTrue(self.board.winnable('machine') == 1, 'Exptected to be able to win')