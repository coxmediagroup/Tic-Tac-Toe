from django.test import SimpleTestCase
import mock

from .board import Board
from .models import Game
from .strategy import RandomStrategy


class BoardTest(SimpleTestCase):
    def test_new_game(self):
        b = Board()
        expected = (
            ' | | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(0, b.state())
        self.assertEqual(Board.MARK_X, b.next_mark())
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertFalse(b.winner())

    def test_one_move(self):
        b = Board(state=1)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertEqual(Board.MARK_O, b.next_mark())
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], b.next_moves())
        self.assertFalse(b.winner())

    def test_row1_winner(self):
        b = Board(state=14755)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            ' |O| \n'
            '-+-+-\n'
            'O| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())
        self.assertEqual(Board.BLANK, b.next_mark())
        self.assertEqual([], b.next_moves())

    def test_row2_winner(self):
        b = Board(state=9453)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|O|O\n'
            '-+-+-\n'
            ' |X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_row3_winner(self):
        b = Board(state=9695)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            'X|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_col1_winner(self):
        b = Board(state=10343)
        expected = (
            'O| | \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X|X')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_col2_winner(self):
        b = Board(state=3783)
        expected = (
            ' |X| \n'
            '-+-+-\n'
            'O|X| \n'
            '-+-+-\n'
            'O|X| ')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_col3_winner(self):
        b = Board(state=14439)
        expected = (
            ' |X|O\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_rising_slash_winner(self):
        b = Board(state=14427)
        expected = (
            ' | |X\n'
            '-+-+-\n'
            ' |X|O\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_falling_slash_winner(self):
        b = Board(state=14267)
        expected = (
            'O| |X\n'
            '-+-+-\n'
            ' |O|X\n'
            '-+-+-\n'
            'X| |O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_O, b.winner())

    def test_two_way_winner(self):
        self.assertRaises(ValueError, Board, state=715)
        b = Board(state=18859)
        expected = (
            'X|X|X\n'
            '-+-+-\n'
            'O|X|O\n'
            '-+-+-\n'
            'X|O|O')
        self.assertMultiLineEqual(expected, str(b))
        self.assertEqual(Board.MARK_X, b.winner())

    def test_two_winners_raises(self):
        self.assertRaises(ValueError, Board, state=715)
        # This corresponds to this board:
        # X|X|X #
        # -+-+- #
        # O|O|O #
        # -+-+- #
        #  | |  #

    def test_large_state_raises(self):
        self.assertRaises(ValueError, Board, state=pow(3, 9))

    def test_O_first_raises(self):
        self.assertRaises(ValueError, Board, state=2)

    def test_too_many_X_raises(self):
        self.assertRaises(ValueError, Board, state=4)

    def test_valid_move(self):
        b = Board()
        b.move(0)
        expected = (
            'X| | \n'
            '-+-+-\n'
            ' | | \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(b))
        self.assertEqual(1, b.state())
        self.assertFalse(b.winner())

    def test_invalid_move_raises(self):
        b = Board(state=1)
        self.assertRaises(ValueError, b.move, 0)


class GameModelTests(SimpleTestCase):
    '''Game tests that do not require a database'''
    def test_get_board(self):
        game = Game(state=220)
        board = game.board
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(board))
        self.assertEqual(220, board.state())

    def test_set_board_in_progress(self):
        board = Board(state=220)
        game = Game()
        game.board = board
        self.assertEqual(220, game.state)
        self.assertEqual(Game.IN_PROGRESS, game.winner)

    def test_set_board_winner(self):
        board = Board(state=18859)
        game = Game()
        game.board = board
        self.assertEqual(18859, game.state)
        self.assertEqual(Game.X_WINS, game.winner)

    def test_random_strategy(self):
        game = Game(strategy_type=Game.RANDOM_STRATEGY)
        strategy = game.strategy
        self.assertTrue(isinstance(strategy, RandomStrategy))


class RandomStrategyTest(SimpleTestCase):
    @mock.patch('tictactoe.strategy.random_choice')
    def test_random_move(self, mock_choice):
        board = Board(state=220)
        expected = (
            'X|X| \n'
            '-+-+-\n'
            'O|O| \n'
            '-+-+-\n'
            ' | | ')
        self.assertEqual(expected, str(board))
        strategy = RandomStrategy()
        mock_choice.return_value = 7

        move = strategy.next_move(board)
        self.assertEqual(7, move)
        mock_choice.assert_called_once_with([2, 5, 6, 7, 8])
