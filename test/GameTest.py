import unittest
import sys
import mock
from cStringIO import StringIO
from contextlib import contextmanager

import game
from TicTacToeExceptions import *

class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = game.Game()

    def tearDown(self):
       self.game = None

    @contextmanager
    def capture(self, command, *args, **kwargs):
        """So we can test print statments"""
        out, sys.stdout = sys.stdout, StringIO()
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
        sys.stdout = out

    def test_computer_move(self):
        """Do we get the correct values when we call player move?"""

        expected = '\n\n | | \n_____\n |X| \n_____\n | | \n\n\nThe computer has beaten you! You lose.\n'
        self.game.board._raw_input = mock.Mock(return_value=1)
        self.game.board.firstMove = mock.Mock(return_value='computer')
        self.game.board.computer_token = 'X'
        self.game.board.isWinner = mock.Mock(return_value='win')
        with self.capture(self.game._computer_move) as output:
            self.assertEqual(output, expected)

        result = self.game._computer_move()
        self.assertEqual(result, True)

        self.game.board.isWinner = mock.Mock(return_value='draw')
        expected = '\n\nX|X| \n_____\n |X| \n_____\n | | \n\n\nThe game is a tie!\n'
        with self.capture(self.game._computer_move) as output:
            self.assertEqual(output, expected)
        result = self.game._computer_move()
        self.assertEqual(result, True)

        self.game.board.isWinner = mock.Mock(return_value=None)
        result = self.game._computer_move()
        self.assertEqual(result, False)


    def test_player_move(self):
        """Do we get the correct values when we call player move?"""

        expected = 'What is your next move? (1-9)\n\n\nX| | \n_____\n | | \n_____\n | | \n\n\nHooray! You have won the game!\n'
        self.game.board._raw_input = mock.Mock(return_value=1)
        self.game.board.firstMove = mock.Mock(return_value='player')
        self.game.board.player_token = 'X'
        self.game.board.isWinner = mock.Mock(return_value='win')
        with self.capture(self.game._player_move) as output:
            self.assertEqual(output, expected)

        self.game.board._raw_input = mock.Mock(return_value=2)
        result = self.game._player_move()
        self.assertEqual(result, True)

        expected = 'What is your next move? (1-9)\n\n\nX|X|X\n_____\n | | \n_____\n | | \n\n\nThe game is a tie!\n'
        self.game.board._raw_input = mock.Mock(return_value=3)
        self.game.board.isWinner = mock.Mock(return_value='draw')
        with self.capture(self.game._player_move) as output:
            self.assertEqual(output, expected)
        result = self.game._player_move()
        self.assertEqual(result, True)

        self.game.board._raw_input = mock.Mock(return_value=4)
        self.game.board.isWinner = mock.Mock(return_value=None)
        result = self.game._player_move()
        self.assertEqual(result, False)


    def test_toggle_turn(self):
        """Do we toggle the player turn correctly?"""

        self.game.current_player = 'player'
        self.game._toggle_turn()
        self.assertEqual(self.game.current_player, 'computer')
        self.game._toggle_turn()
        self.assertEqual(self.game.current_player, 'player')


    def test_print_message(self):
        """Can we print a message?"""

        args = "Test Message"
        with self.capture(self.game._print_message, args) as output:
            self.assertEqual(output, "Test Message\n")
