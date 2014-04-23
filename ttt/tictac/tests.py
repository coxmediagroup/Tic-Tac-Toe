from django.test import TestCase

from tictac.models import Board, Game


class BoardTestCase(TestCase):

    def setUp(self):
        self.tictac1 = Board(rows=3, columns=3)

    def testBoardState(self):
        self.assertEqual(len(self.tictac1.state), 9,
            "Expected 3x3 board to have state 9 chars long, got %d." % (
                len(self.tictac1.state, )))


class GameTestCase(TestCase):

    def setUp(self):
        pass


