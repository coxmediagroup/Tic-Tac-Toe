import unittest
from . import exceptions as ex
from . import Board, naught_bot


class BoardTests(unittest.TestCase):
    """
    Tests showing the rules of the game are being respected.
    """
    def test_board_is_empty_by_default(self):
        game = Board()
        self.assertTrue(all(cell is game.EMPTY for cell in game.cells))

    def test_board_needs_to_know_who_marked_first_when_setting_initial_state(self):
        with self.assertRaises(ex.FirstPlayerRequiredError):
            Board([Board.EMPTY, ] * 9)

    def test_board_must_have_nine_cells(self):
        for count in xrange(0, 8):
            with self.assertRaises(ex.SizeError):
                Board([Board.EMPTY, ] * count, first_player=Board.NAUGHT)

    def test_board_raises_when_marking_a_non_empty_cell(self):
        game = Board()
        game[0] = game.NAUGHT

        with self.assertRaises(ex.NonEmptyCellError):
            game[0] = game.CROSS

    def test_game_wont_allow_two_moves_in_a_row_from_either_player(self):
        game = Board()
        game[0] = game.CROSS
        with self.assertRaises(ex.DoubleMoveError):
            game[1] = game.CROSS

        game[1] = game.NAUGHT
        with self.assertRaises(ex.DoubleMoveError):
            game[2] = game.NAUGHT


    def test_game_knows_when_cross_wins(self):
        x, o, _ = Board.CROSS, Board.NAUGHT, Board.EMPTY
        game = Board([x, _, o,
                      x, o, x,
                      _, o, _],
                     first_player=x)
        with self.assertRaises(ex.GameOver) as ctx:
            game[6] = x

        self.assertEqual(game.winner, x)
        self.assertEqual(ctx.exception.winner, x)

    def test_game_knows_when_naught_wins(self):
        x, o, _ = Board.CROSS, Board.NAUGHT, Board.EMPTY
        game = Board([o, _, x,
                      o, x, o,
                      _, x, _],
                     first_player=o)
        with self.assertRaises(ex.GameOver) as ctx:
            game[6] = o

        self.assertEqual(game.winner, o)
        self.assertEqual(ctx.exception.winner, o)

    def test_game_board_cannot_be_modified_once_it_has_been_won(self):
        x, o, _ = Board.CROSS, Board.NAUGHT, Board.EMPTY
        game = Board([x, _, o,
                      x, o, x,
                      _, o, _],
                     first_player=x)
        with self.assertRaises(ex.GameOver):
            game[6] = x

        with self.assertRaises(ex.GameOver):
            # this change should be rolled back
            game[8] = o

        self.assertEqual(game[8], game.EMPTY)


class NaughtBotStartsTests(unittest.TestCase):
    """
    Tests demonstrating naught_bot's decision-making process.
    """
    def test_knows_how_to_open_first(self):
        game = Board()
        self.assertEqual(naught_bot(game), 4)

    def test_knows_when_to_block(self):
        x, o, _ = Board.CROSS, Board.NAUGHT, Board.EMPTY
        game = Board([_, _, _,
                      x, x, _,
                      o, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (5,))
        game = Board([o, _, _,
                      _, x, _,
                      x, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (2,))
        game = Board([o, x, o,
                      _, x, _,
                      x, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (7,))

    def test_knows_when_to_attack(self):
        x, o, _ = Board.CROSS, Board.NAUGHT, Board.EMPTY
        game = Board([o, _, x,
                      _, o, _,
                      x, x, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (8,))
