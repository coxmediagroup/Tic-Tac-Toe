import unittest
import sys
from cStringIO import StringIO
from contextlib import contextmanager

import game
from TicTacToeExceptions import *

class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = game.Game()

    def tearDown(self):
       self.board = None

    @contextmanager
    def capture(self, command, *args, **kwargs):
        """So we can test print statments"""
        out, sys.stdout = sys.stdout, StringIO()
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
        sys.stdout = out

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
