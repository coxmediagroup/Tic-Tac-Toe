import unittest
from .exceptions import SizeError, DoubleMoveError, NonEmptyCellError, FirstPlayerRequiredError
from . import Board, naught_bot


class BoardTests(unittest.TestCase):
    """
    Tests showing the rules of the game are being respected.
    """
    def test_board_is_empty_by_default(self):
        game = Board()
        self.assertTrue(all(cell is game.EMPTY for cell in game.cells))

    def test_board_needs_to_know_who_marked_first_when_setting_initial_state(self):
        with self.assertRaises(FirstPlayerRequiredError):
            Board([Board.EMPTY, ] * 9)

    def test_board_must_have_nine_cells(self):
        for count in xrange(0, 8):
            with self.assertRaises(SizeError):
                Board([Board.EMPTY, ] * count, first_player=Board.NAUGHT)

    def test_board_raises_when_marking_a_non_empty_cell(self):
        game = Board()
        game[0] = game.NAUGHT

        with self.assertRaises(NonEmptyCellError):
            game[0] = game.CROSS

    def test_game_wont_allow_two_moves_in_a_row_from_either_player(self):
        game = Board()
        game[0] = game.CROSS
        with self.assertRaises(DoubleMoveError):
            game[1] = game.CROSS

        game[1] = game.NAUGHT
        with self.assertRaises(DoubleMoveError):
            game[2] = game.NAUGHT


class NaughtBotTests(unittest.TestCase):
    """
    Tests demonstrating naught_bot's decision-making process.
    """
    def test_knows_if_it_went_first(self):
        raise NotImplementedError

    def test_knows_if_it_went_second(self):
        raise NotImplementedError

    def test_knows_when_to_block(self):
        raise NotImplementedError

    def test_knows_when_to_push_for_a_win(self):
        raise NotImplementedError