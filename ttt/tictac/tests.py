
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

    def testBoardValidMove(self):
        pass


    def testBoardCanPlay(self):
        pass

    def testBoardMarkPlay(self):
        pass


class GameTestCase(TestCase):

    def setUp(self):
        self.tictac1 = Board(rows=3, columns=3)
        self.game = Game.objects.new_game(game_type='classic', players=[
            { 'name':'Baron' },
            { 'name':'Joshua', 'auto': True, }, ])
        self.game.save()

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

    def testWinner(self):
        self.game.board.state = '123456789'

        result = self.game.has_winning_board(debug=True)
        self.assertEqual(result[0], ('123', False))
        self.assertEqual(result[1], ('456', False))
        self.assertEqual(result[2], ('789', False))
        self.assertEqual(result[3], ('147', False))
        self.assertEqual(result[4], ('258', False))
        self.assertEqual(result[5], ('369', False))
        self.assertEqual(result[6], ('159', False))
        self.assertEqual(result[7], ('357', False))
        self.assertFalse(self.game.has_winning_board(), 'Board %s should have no winner: \n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122122211'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

    def testNextPlayer(self):
        pass

    def testMakePlay(self):
        pass

