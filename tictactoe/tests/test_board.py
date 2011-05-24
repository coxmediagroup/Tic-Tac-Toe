import unittest2 as unittest

from tictactoe.board import Board


class TestBoard(unittest.TestCase):

    def test_add_move_fails_for_invalid_move(self):
        with self.assertRaises(ValueError):
            Board().add_move('n', 0)

    def test_add_move_succeeds_for_valid_move(self):
        board = Board()
        board.add_move(board.x, 0)
        self.assertEqual(board.last_player, board.x, 'Last player not set')
        self.assertEqual(board.state[0], board.x, 'Position not set')

    def test_check_move_fails_for_invalid_player(self):
        with self.assertRaises(ValueError):
            Board().add_move('z', 0)

    def test_check_move_fails_for_out_of_turn_player(self):
        with self.assertRaises(ValueError):
            board = Board()
            board.add_move(board.x, 0)
            board.add_move(board.x, 0)

    def test_check_move_fails_for_invalid_position(self):
        with self.assertRaises(ValueError):
            Board().add_move(Board.x, 15)

    def test_get_opponent(self):
        self.assertEqual(Board.get_opponent(Board.x), Board.o, 'Wrong opponent')

    def test_get_winner_returns_player_for_win(self):
        board = Board(state=[x for x in 'xoo x   x'])
        self.assertEquals(board.get_winner(), board.x,
                          'Incorrect winner determined')

    def test_get_winner_returns_none_for_draw(self):
        board = Board(state=[x for x in 'xoooxxxoo'])
        self.assertEquals(board.get_winner(), None,
                          'Winner incorrectly determined')

    def test_get_winner_returns_none_for_unfinished_game(self):
        board = Board(state=[x for x in 'x         '])
        self.assertEquals(board.get_winner(), None,
                          'Winner incorrectly determined')

    def test_is_game_over_returns_true_for_no_more_moves(self):
        board = Board(state=['x'] * 9)
        self.assertTrue(board.is_game_over(), 'Game should be over')

    def test_iter_rows(self):
        board = Board()
        board.add_move(board.x, 0)
        rows = list(board.iter_rows())
        expected_rows = [
            ['x', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '],
            ['x', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' '],
            ['x', ' ', ' '], [' ', ' ', ' ']]
        self.assertEqual(rows, expected_rows, 'Invalid row iteration')

    def test_printable_state(self):
        board = Board()
        board.add_move(board.x, 8)
        expected = board.board_template % tuple([' '] * 8 + ['x'])
        self.assertEqual(expected, board.printable_state,
                         'Printable state not as expected')

    def test_valid_moves_for_empty_board(self):
        self.assertEqual(list(xrange(9)), Board().valid_moves,
                         'Incorrect moves for empty board')

    def test_valid_moves_for_non_empty_board(self):
        board = Board()
        board.add_move(board.x, 0)
        self.assertEqual(list(xrange(9))[1:], board.valid_moves,
                         'Incorrect moves for non-empty board')
