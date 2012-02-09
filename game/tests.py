from django.test  import TestCase
from django.utils import simplejson

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
        g.save()

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
        g.save()

        assert g._board.upper_left  == PLAYER_X
        assert g._board.center_left == PLAYER_O

    def test_x_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        with self.assertRaises(Exception):
            g[0][1] = PLAYER_X

    def test_o_goes_out_of_turn(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        with self.assertRaises(Exception):
            g[0][2] = PLAYER_O

    def test_dup_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
        g[0][1] = PLAYER_O
        with self.assertRaises(Exception):
            g[0][0] = PLAYER_X

    def test_stomp_move(self):
        """
        Tests that a game board can be modified via indexing
        """

        g = Game.create_new()
        g[0][0] = PLAYER_X
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
        assert win == (0,2)
    
    def test_x_blocker_rev_diag(self):
        """
        Test if there is a winning move along the reverse diag (to block x)
        """

        g = Game.create_new()
        g[0][2] = PLAYER_X
        g[1][0] = PLAYER_O
        g[1][1] = PLAYER_X

        win = g.winning_move(for_player=PLAYER_X)
        assert win == (2,0)

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
        assert win == (2,1)

class ViewTest(TestCase):
    def setUp(self):
        Game.create_new()
        Game.create_new()
        Game.create_new()

        assert Game.objects.count() == 3
        
        self.max_id = 3

    def test_get_all_root(self):
        response = self.client.get('')

        assert response.status_code == 200
        assert len(response.context['games']) == 3
        assert response.context['games'][0].id == 1
        assert response.context['games'][1].id == 2
        assert response.context['games'][2].id == 3

    def test_get_all(self):
        response = self.client.get('/game/')

        assert response.status_code == 200
        assert len(response.context['games']) == 3
        assert response.context['games'][0].id == 1
        assert response.context['games'][1].id == 2
        assert response.context['games'][2].id == 3

    def test_create_new(self):
        response = self.client.post('/game/new')
        self.assertRedirects(response, '/game/%d/' % (self.max_id+1))

    def test_get_game(self):
        response = self.client.get('/game/1/')

        assert response.status_code == 200
        assert type(response.context['game']) == Game

    def test_post_move(self):
        response = self.client.post('/game/1/move', 
                                    {'player':'x', 'col': 0, 'row': 0 })
        self.assertRedirects(response, '/game/1/')

        response = self.client.get('/game/1/')

        assert response.status_code == 200
        assert type(response.context['game']) == Game
        assert response.context['game'][0][0] == PLAYER_X

    def test_post_move_by_ajax(self):
        response = self.client.post('/game/2/move', 
                                    {'player':'x', 'col': 0, 'row': 0 },
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    )
        assert response.status_code == 200
        content = simplejson.loads(response.content)
        assert content['player'] == 'o'
        assert 'col' in content
        assert 'row' in content

