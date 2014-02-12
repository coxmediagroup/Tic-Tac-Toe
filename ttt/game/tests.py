from django.test import TestCase
import json

from game.models import *
from game.player import Computer


class GameTest(TestCase):
    def test_basic_game_creation(self):
        """
        Demonstrate you can create a Game object directly
        But accessing the board without prior initialization
        raises an exception
        """
        g = Game()
        assert g is not None
        g.save()

        g = Game.objects.get(pk=g.id)
        with self.assertRaises(Board.DoesNotExist):
            board = g._board

    def test_game_creation_method(self):
        """
        Tests that a method in Game built for kosher creation succeeds
        """
        g = Game.create_new()
        assert g is not None
        assert g._board is not None

    def test_illegal_board_indices(self):
        g = Game.create_new()
        with self.assertRaises(Exception):
            ill = g[-1]
        with self.assertRaises(Exception):
            ill = g[3]
        with self.assertRaises(Exception):
            ill = g[0][-1]
        with self.assertRaises(Exception):
            ill = g[0][3]
        with self.assertRaises(Exception):
            g[0][-1] = PLAYER_X
        with self.assertRaises(Exception):
            g[0][3] = PLAYER_X

    def test_illegal_board_values(self):
        g = Game.create_new()
        with self.assertRaises(Exception):
            g[0][0] = -2
        with self.assertRaises(Exception):
            g[0][0] = -1.1
        with self.assertRaises(Exception):
            g[0][0] = 0.5
        with self.assertRaises(Exception):
            g[0][0] = 1.1
        with self.assertRaises(Exception):
            g[0][0] = 2
        with self.assertRaises(Exception):
            g[0][0] = PLAYER_NONE
        with self.assertRaises(Exception):
            g[0][0] = None
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O

    def test_x_goes_first(self):
        """
        Test that x gets to make the first move
        """
        g = Game.create_new()
        g[0][0] = PLAYER_X
        assert g._board.upper_left == PLAYER_X

    def test_o_goes_first(self):
        """
        Test that o gets to make the first move
        """
        g = Game.create_new()

        with self.assertRaises(Exception):
            g[0][0] = PLAYER_O

    def test_two_valid_moves(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O

        g = Game.objects.get(pk=g.id)
        assert g._board.upper_left == PLAYER_X
        assert g._board.center_left == PLAYER_O

    def test_x_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X

        g = Game.objects.get(pk=g.id)
        with self.assertRaises(Exception):
            g[0][1] = PLAYER_X

    def test_o_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O

        g = Game.objects.get(pk=g.id)
        with self.assertRaises(Exception):
            g[0][2] = PLAYER_O

    def test_dup_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O

        g = Game.objects.get(pk=g.id)
        with self.assertRaises(Exception):
            g[0][0] = PLAYER_X

    def test_stomp_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X

        g = Game.objects.get(pk=g.id)
        with self.assertRaises(Exception):
            g[0][0] = PLAYER_O

    def test_no_win_complete(self):
        """
        Test if the game is complete when game board is filled and no winner
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        g[0][2] = PLAYER_X
        g[1][0] = PLAYER_O
        g[1][1] = PLAYER_X
        g[2][0] = PLAYER_O
        g[1][2] = PLAYER_X
        g[2][2] = PLAYER_O
        g[2][1] = PLAYER_X

        g = Game.objects.get(pk=g.id)
        assert g.is_complete()
        assert g.who_won() == PLAYER_NONE

    def test_x_wins(self):
        """
        Test if the game is complete when game board is filled and no winner
        """
        from datetime import datetime

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O
        g[0][1] = PLAYER_X
        g[1][1] = PLAYER_O
        g[0][2] = PLAYER_X

        g = Game.objects.get(pk=g.id)

        delta = datetime.now() - g.ended if g.ended is not None else None

        assert delta is not None
        assert delta.seconds < 2
        assert g.is_complete()
        assert g.who_won() == PLAYER_X
        with self.assertRaises(Exception):
            g[1][2] = PLAYER_O

    def test_o_wins(self):
        """
        Test if the game is complete when game board is filled and no winner
        """
        from datetime import datetime

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O
        g[0][1] = PLAYER_X
        g[1][1] = PLAYER_O
        g[2][2] = PLAYER_X
        g[1][2] = PLAYER_O

        g = Game.objects.get(pk=g.id)

        delta = datetime.now() - g.ended if g.ended is not None else None

        assert delta is not None
        assert delta.seconds < 2
        assert g.is_complete()
        assert g.who_won() == PLAYER_O
        with self.assertRaises(Exception):
            g[0][2] = PLAYER_X

    def test_x_winning_move_col_0(self):
        """
        Test if there is a winning move for x along a column
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O
        g[0][1] = PLAYER_X
        g[1][1] = PLAYER_O

        win = g.winning_move(for_player=PLAYER_X)
        assert win == (0, 2)

    def test_x_blocker_rev_diag(self):
        """
        Test if there is a winning move along the reverse diag (to block x)
        """

        g = Game.create_new()
        g[0][2] = PLAYER_X
        g[1][0] = PLAYER_O
        g[1][1] = PLAYER_X

        win = g.winning_move(for_player=PLAYER_X)
        assert win == (2, 0)

    def test_o_winning_move_row(self):
        """
        Test if there is a winning move along a row for o
        """

        g = Game.create_new()
        g[0][2] = PLAYER_X
        g[0][1] = PLAYER_O
        g[2][0] = PLAYER_X
        g[1][1] = PLAYER_O
        g[0][0] = PLAYER_X

        win = g.winning_move(for_player=PLAYER_O)
        assert win == (2, 1)


class ComputerTest(TestCase):
    def test_first_move_as_x(self):
        g = Game.create_new(is_user_x=False)
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 1)

    def test_first_move_as_o(self):
        g = Game.create_new(is_user_x=True)
        g[0][0] = PLAYER_X
        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (1, 1)

    def test_first_move_as_o_with_x_in_center(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X
        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)

    def test_vertical_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[1][0] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (1, 2)

    def test_horizontal_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[0][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (2, 1)

    def test_diagonal_block(self):
        g = Game.create_new(is_user_x=True)
        g[1][1] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 0)
        g[move[0]][move[1]] = PLAYER_O

        g[2][0] = PLAYER_X

        move = Computer.determine_move(g, PLAYER_O, PLAYER_X)
        assert move == (0, 2)

    def test_guaranteed_win_scenario(self):
        g = Game.create_new(is_user_x=False)
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 1)
        g[move[0]][move[1]] = PLAYER_X

        # any center border cell will do here
        # this first move by the opposite player guarantees a win
        g[0][1] = PLAYER_O

        # the next move should be in an adjacent corner
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (0, 0) or move == (0, 2)
        g[move[0]][move[1]] = PLAYER_X

        # This move has created a potential win right away
        winning_move = g.winning_move(for_player=PLAYER_X)
        assert winning_move == (2, 0) or winning_move == (2, 2)

        g[winning_move[0]][winning_move[1]] = PLAYER_O

        # the computer's next move should be adjacent to his two previous plays
        move = Computer.determine_move(g, PLAYER_X, PLAYER_O)
        assert move == (1, 0) or move == (1, 2)

        #if we have gotten here, then we know the algorithms are working


