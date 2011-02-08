from django.test import TestCase
from game.models import Game

class GameTest(TestCase):
    """
    Unit tests for Game model.
    """
    def test_get_winner_empty_board(self):
        "An empty board has no winner."
        g = Game()
        self.assertEquals(g.get_winner(), None)

    def test_get_winner_diagonal(self):
        "Three on a diagonal is a winner."
        g = Game()

        g.board_state = [['X', None, None],
                         [None, 'X', None],
                         [None, None, 'X']]
        self.assertEquals(g.get_winner(), 'X')

        g.board_state = [[None, None, 'O'],
                         [None, 'O', None],
                         ['O', None, None]]
        self.assertEquals(g.get_winner(), 'O')

    def test_get_winner_rows(self):
        "Three in a row is a winner."
        for i in xrange(0, 3):
            g = Game()
            g.board_state[i][0] = g.board_state[i][1] = g.board_state[i][2] = 'X'
            self.assertEquals(g.get_winner(), 'X')

            g = Game()
            g.board_state[i][0] = g.board_state[i][1] = g.board_state[i][2] = 'O'
            self.assertEquals(g.get_winner(), 'O')

    def test_get_winner_column(self):
        "Three in a column is a winner."
        for i in xrange(0, 3):
            g = Game()
            g.board_state[0][i] = g.board_state[1][i] = g.board_state[2][i] = 'X'
            self.assertEquals(g.get_winner(), 'X')

            g = Game()
            g.board_state[0][i] = g.board_state[1][i] = g.board_state[2][i] = 'O'
            self.assertEquals(g.get_winner(), 'O')

    def test_is_game_over_empty(self):
        "An empty game board is not game over."
        g = Game()
        self.assertFalse(g.is_game_over())

    def test_is_game_over_winner(self):
        "A game board with a winner is a game over."
        g = Game()
        g.board_state[0][0] = g.board_state[0][1] = g.board_state[0][2] = 'X'
        self.assertTrue(g.is_game_over())

    def test_is_game_over_tie(self):
        "A game board that is a tie is a game over."
        g = Game()
        g.board_state = [['X', 'O', 'X'],
                         ['X', 'O', 'X'],
                         ['O', 'X', 'O']]
        self.assertTrue(g.is_game_over())
