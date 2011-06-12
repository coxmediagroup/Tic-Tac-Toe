
from django.test import TestCase

class TicTacToeTests(TestCase):
    """
    Unit tests for the TicTacToe class.
    """
    def setUp(self):
        import game
        self.ttt_x = game.TicTacToe('X')
        self.ttt_o = game.TicTacToe('O')

    def test_invalid_tictactoe_side_raises_valueerror(self):
        import game
        self.assertRaises(ValueError, game.TicTacToe, 'T')

    def test_tictactoe_deepcopies_board_instead_of_mutating_initial_state(self):
        empty_board = [[' ', ' ', ' '],
                       [' ', ' ', ' '],
                       [' ', ' ', ' ']]
        updated_board = self.ttt_x.make_move(empty_board)
        self.assertFalse(updated_board is empty_board)

    def test_empty_board_o_cannot_make_a_choice(self):
        empty_board = [[' ', ' ', ' '],
                       [' ', ' ', ' '],
                       [' ', ' ', ' ']]
        self.assertRaises(ValueError, self.ttt_o.make_move, empty_board)

    def test_empty_board_x_can_make_a_choice(self):
        empty_board = [[' ', ' ', ' '],
                       [' ', ' ', ' '],
                       [' ', ' ', ' ']]
        self.assertTrue(isinstance(self.ttt_x.make_move(empty_board), list))

    def test_board_with_five_choices_3x_2o_allows_o_to_choose(self):
        board = [['X', 'O', ' '],
                 [' ', 'X', ' '],
                 ['X', ' ', 'O']]
        self.assertTrue(isinstance(self.ttt_o.make_move(board), list))

    def test_board_with_five_choices_3x_2o_raises_error_when_x_chooses(self):
        board = [['X', 'O', ' '],
                 [' ', 'X', ' '],
                 ['X', ' ', 'O']]
        self.assertRaises(ValueError, self.ttt_x.make_move, board)

    def test_board_with_five_choices_4x_1o_raises_error_when_x_chooses(self):
        board = [['X', 'O', ' '],
                 [' ', 'X', 'X'],
                 ['X', ' ', ' ']]
        self.assertRaises(ValueError, self.ttt_x.make_move, board)

    def test_board_with_five_choices_4x_1o_raises_error_when_o_chooses(self):
        board = [['X', 'O', ' '],
                 [' ', 'X', 'X'],
                 ['X', ' ', ' ']]
        self.assertRaises(ValueError, self.ttt_o.make_move, board)

    def test_game_chooses_winning_move_when_available(self):
        board = [['X', 'O', 'X'],
                 [' ', 'X', 'O'],
                 ['O', ' ', ' ']]
        updated_board = self.ttt_x.make_move(board)
        self.assertEqual(updated_board[0], ['X', 'O', 'X'])
        self.assertEqual(updated_board[1], [' ', 'X', 'O'])
        self.assertEqual(updated_board[2], ['O', ' ', 'X'])

    def test_game_prevents_winning_opponents(self):
        board = [['X', 'O', 'O'],
                 ['O', 'X', 'X'],
                 ['X', ' ', ' ']]
        updated_board = self.ttt_o.make_move(board)
        self.assertEqual(updated_board[0], ['X', 'O', 'O'])
        self.assertEqual(updated_board[1], ['O', 'X', 'X'])
        self.assertEqual(updated_board[2], ['X', ' ', 'O'])

    def test_winner_returns_none_if_no_winner(self):
        board = [['X', 'O', 'O'],
                 ['O', 'X', 'X'],
                 ['X', ' ', ' ']]
        self.assertEqual(self.ttt_x.winner(board), None)

    def test_winner_returns_x_if_x_wins(self):
        board = [['X', 'O', 'O'],
                 ['O', 'X', 'X'],
                 [' ', ' ', 'X']]
        self.assertEqual(self.ttt_x.winner(board), 'X')

    def test_winner_returns_o_if_o_wins(self):
        board = [['O', 'O', 'O'],
                 [' ', 'X', 'X'],
                 [' ', ' ', 'X']]
        self.assertEqual(self.ttt_x.winner(board), 'O')

    def test_winner_returns_space_if_tie(self):
        board = [['O', 'X', 'X'],
                 ['X', 'X', 'O'],
                 ['O', 'O', 'X']]
        self.assertEqual(self.ttt_x.winner(board), ' ')
