from django.test import TestCase
from game.models import Game
from game.ai import perform_move

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

class AITests(TestCase):
    """
    Unit tests for AI.
    """
    def test_take_win(self):
        "The AI should always take a winning move if available."
        # Row
        g = Game()
        g.board_state[0][0] = g.board_state[0][1] = 'X'
        perform_move(g)
        self.assertEquals(g.board_state[0][2], 'X')

        # Col
        g = Game()
        g.board_state[0][0] = g.board_state[1][0] = 'X'
        perform_move(g)
        self.assertEquals(g.board_state[2][0], 'X')

        # Diagonals
        g = Game()
        g.board_state[0][2] = g.board_state[2][0] = 'X'
        perform_move(g)
        self.assertEquals(g.board_state[1][1], 'X')

        g = Game()
        g.board_state[0][0] = g.board_state[1][1] = 'X'
        perform_move(g)
        self.assertEquals(g.board_state[2][2], 'X')

        g = Game()
        g.board_state[2][0] = g.board_state[1][1] = 'X'
        perform_move(g)
        self.assertEquals(g.board_state[0][2], 'X')

    def test_take_block(self):
        "The AI should always block the player if possible."
        # Row
        g = Game()
        g.board_state[0][0] = g.board_state[0][1] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[0][2], 'X')

        # Col
        g = Game()
        g.board_state[0][0] = g.board_state[1][0] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[2][0], 'X')

        # Diagonals
        g = Game()
        g.board_state[0][2] = g.board_state[2][0] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[1][1], 'X')

        g = Game()
        g.board_state[0][0] = g.board_state[1][1] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[2][2], 'X')

        g = Game()
        g.board_state[2][0] = g.board_state[1][1] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[0][2], 'X')

    def test_first_move(self):
        "The AI should always take the middle cell if it is the first move."
        g = Game()
        perform_move(g)
        self.assertEquals(g.board_state[1][1], 'X')

    def test_second_move(self):
        """
        The AI should always try for the middle cell, but fallback to any
        corner if it is taken.
        """
        g = Game()
        g.board_state[0][1] = 'O'
        perform_move(g)
        self.assertEquals(g.board_state[1][1], 'X')

        g = Game()
        g.board_state[1][1] = 'O'
        perform_move(g)
        corners = [
            g.board_state[0][0], g.board_state[0][2],
            g.board_state[2][0], g.board_state[2][2]
        ]
        self.assertTrue('X' in set(corners))
