
from django.db import transaction
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
        self.tictac1 = Board(rows=3, columns=3)
        self.game = Game.objects.new_game(game_type='classic', players=[
            { 'name':'Baron' },
            { 'name':'Joshua', 'auto': True, }, ])

    def testGameType(self):
        self.assertEqual(self.game.game_type, 'classic')
        self.assertEqual(self.game.board.rows, self.game.board.columns,
            'Expected classic board to be square, but it was %d x %d.' % (
                self.game.board.rows, self.game.board.columns))
        self.assertEqual(self.game.board.rows * self.game.board.columns, 9,
            'Expected classic board to be 3x3, but it was %d x %d.' % (
                self.game.board.rows, self.game.board.columns))

    def testGameAssertions(self):
        # Only supports classic
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Game.objects.new_game(game_type='bogus')

        # Can only do two players at most
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Game.objects.new_game(game_type='classic', players=[
                    { 'name':'Baron' },
                    { 'name':'Joshua', 'auto': True, },
                    { 'name':'OneTooMany'}, ])

        # gotta have at least 1 player!
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Game.objects.new_game(game_type='classic', players=[], )

    def testOnePlayerGame(self):
        ok = Game.objects.new_game(game_type='classic', players=[
                    { 'name':'Baron' }, ])
        self.assertEqual(ok.players.count(), 1, 'Expected one player, but got %d' % (
            ok.players.count()))

