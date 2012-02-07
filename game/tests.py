from django.test import TestCase

from tictactoe.game.models import *

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
        with self.assertRaises(Board.DoesNotExist):
            board = g._board

    def test_game_creation_method(self):
        """
        Tests that a method in Game built for kosher creation succeeds
        """"
        g = Game.create_new()
        assert g is not None
        assert g._board is not None

    def test_illegal_board_indices(self):
        g = Game.create_new()
        with self.assertRaise(Exception):
          ill = g[-1]
        with self.assertRaise(Exception):
          ill = g[3]
        with self.assertRaise(Exception):
          ill = g[0][-1]
        with self.assertRaise(Exception):
          ill = g[0][3]
        with self.assertRaise(Exception):
          g[0][-1] = PLAYER_X
        with self.assertRaise(Exception):
          g[0][3] = PLAYER_X

    def test_illegal_board_values(self):
        g = Game.create_new()
        with self.assertRaise(Exception):
          g[0][0] = -2
        with self.assertRaise(Exception):
          g[0][0] = -1.1
        with self.assertRaise(Exception):
          g[0][0] = 0.5
        with self.assertRaise(Exception):
          g[0][0] = 1.1
        with self.assertRaise(Exception):
          g[0][0] = 2
        with self.assertRaise(Exception):
          g[0][0] = PLAYER_NONE
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O
        g.save()

    def test_x_goes_first(self):
        """
        Test that x gets to make the first move
        """
        g[0][0] = PLAYER_X
        assert g._board.upper_left == PLAYER_X

    def test_o_goes_first(self):
        """
        Test that o gets to make the first move
        """
        with self.assertRaise(Exception):
            g[0][0] = PLAYER_O

    def test_two_valid_moves(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        g.save()

        assert g._board.upper_left   == PLAYER_X
        assert g._board.upper_center == PLAYER_O

    def test_x_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        with self.assertRaise(Exception):
            g[0][1] = PLAYER_X

    def test_o_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        with self.assertRaise(Exception):
            g[0][2] = PLAYER_O

    def test_dup_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        with self.assertRaise(Exception):
            g[0][0] = PLAYER_X

    def test_stomp_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        with self.assertRaise(Exception):
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

        delta = datetime.now() - g.ended if g.ended is not None else None

        assert delta is not None
        assert delta.seconds < 2
        assert g.is_complete()
        assert g.who_won() == PLAYER_X
        with self.assertRaise(Exception):
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

        delta = datetime.now() - g.ended if g.ended is not None else None

        assert delta is not None
        assert delta.seconds < 2
        assert g.is_complete()
        assert g.who_won() == PLAYER_O
        with self.assertRaise(Exception):
            g[0][2] = PLAYER_X
    
    def test_x_winning_move(self):
        """
        Test if the game is complete when game board is filled and no winner
        """
        from datetime import datetime


        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[1][0] = PLAYER_O
        g[0][1] = PLAYER_X
        g[1][1] = PLAYER_O

        win = g.winning_move(for_player=PLAYER_X)
        assert win == (0,2)
    
    def test_x_blocker(self):
        """
        Test if the game is complete when game board is filled and no winner
        """
        from datetime import datetime


        g = Game.create_new()
        g[0][2] = PLAYER_X
        g[1][0] = PLAYER_O
        g[1][1] = PLAYER_X

        win = g.winning_move(for_player=PLAYER_X)
        assert win == (0,2)

    
