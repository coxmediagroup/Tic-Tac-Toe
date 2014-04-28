
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
        good = Board(rows=3, columns=3)

        self.assertTrue(good.is_valid_move(0, 0), 'Expected to be able to move to 0,0.')
        self.assertTrue(good.is_valid_move(2, 0), 'Expected to be able to move to 2,0.')
        self.assertTrue(good.is_valid_move(2, 2), 'Expected to be able to move to 2,2.')

        self.assertFalse(good.is_valid_move(3, 3), 'Expected move to be declined to 3,0.')
        self.assertFalse(good.is_valid_move(3, 4), 'Expected move to be declined to 4,0.')


    def testBoardCanPlay(self):
        good = Board(rows=3, columns=3)
        good.state = '1 12 2 1 '

        # check valid moves
        go = -1
        spot_open = 0
        while go > spot_open:
            go = spot_open
            spot_open = good.state.index(' ', spot_open)
            r = spot_open / good.columns
            c = spot_open % good.rows
            self.assertTrue(good.can_play(r,c), "Expcted open spot at %d, %d." % (r, c))


    def testBoardMarkPlay(self):
        good = Board(rows=3, columns=3)
        good.state = '0 01 1 0 '

        # Should succeed
        good.mark_play(0,1,0)
        good.mark_play(1,1,1)
        good.mark_play(2,0,0)
        good.mark_play(2,2,0)

        # aldready played; should fail!
        with self.assertRaises(Exception):
            with transaction.atomic():
                good.mark_play(0, 1, 1)
                good.mark_play(1, 1, 0)
                good.mark_play(2, 0, 1)
                good.mark_play(2, 2, 1)

        self.assertEqual(good.state, '000111000',
            "Movs made didn't match: %s != %s" % (good.state, '000111000', ))


class GameTestCase(TestCase):

    def setUp(self):
        self.tictac1 = Board(rows=3, columns=3)
        self.player1_name = 'Baron'
        self.player2_name = 'Joshua'
        self.game = Game.objects.new_game(game_type='classic', players=[
            { 'name':self.player1_name, 'auto': False },
            { 'name':self.player2_name, 'auto': False }, ])
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

        result = self.game.has_winning_board()
        self.assertFalse(self.game.has_winning_board(), 'Board %s should have no winner: \n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122122211'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '111122211'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122111211'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122211111'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122111122'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '212111212'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '221111221'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '122111221'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

        self.game.board.state = '221112122'
        self.assertTrue(self.game.has_winning_board(), 'Board %s should have a winner:\n\n%s' % (
            self.game.board.state, self.game.board.__repr__()))

    def testNextPlayer(self):
        player = self.game.next_gameplayer()
        self.assertEqual(player.player.first_name, self.player1_name, 'Expected player named %s to be up first, got %s instead.' % (self.player1_name, player.player.first_name, ))
        self.assertEqual(player.number, 0, 'Expected player to be player #1 (0), got %d instead.' % (player.number, ))

        # Kick up the turn counter and see if we get player #2
        self.game.turn_counter = self.game.turn_counter + 1
        player = self.game.next_gameplayer()
        self.assertEqual(player.player.first_name, self.player2_name, 'Expected player named %s to be up second, got %s instead.' % (self.player2_name, player.player.first_name, ))
        self.assertEqual(player.number, 1, 'Expected player to be player #2 (1), got %d instead.' % (player.number, ))

        # Kick up the turn counter and see if we get player #2
        self.game.turn_counter = self.game.turn_counter + 1
        player = self.game.next_gameplayer()
        self.assertEqual(player.player.first_name, self.player1_name, 'Expected player named %s to be up third again, got %s instead.' % (self.player1_name, player.player.first_name, ))
        self.assertEqual(player.number, 0, 'Expected player to be player #1 (0) again, got %d instead.' % (player.number, ))

    def testMakePlay(self):

        self.assertEqual(self.game.turn_counter, 0, 'Expected game to be new, not one that had %d turns already run.' % (self.game.turn_counter,))

        self.game.play_turn(0, row=1, column=1)
        self.game.play_turn(1, row=0, column=0)
        self.game.play_turn(0, row=0, column=2)
        self.game.play_turn(1, row=1, column=0)

        self.assertEqual(self.game.board.state, '1 010    ', 'Board does not look like expected.')
        self.assertFalse(self.game.has_winning_board(), 'Game should not be a winner, yet')
        self.assertFalse(self.game.game_over, 'Game not over yet, why is game_over True?')

        self.game.play_turn(0, row=2, column=0)
        self.assertTrue(self.game.has_winning_board(), 'Game now has a winner but we dont see it?')
        self.assertTrue(self.game.game_over, 'Game won, so it should be over.')
        self.assertEqual(self.game.winner, self.game.next_gameplayer().player, 'The next player should be the same as the winner when the game is over.')
