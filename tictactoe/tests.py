import unittest
from . import exceptions as ex
from . import Board, naught_bot, NAUGHT, CROSS, EMPTY

x, o, _ = CROSS, NAUGHT, EMPTY


class BoardTests(unittest.TestCase):
    """
    Tests showing the rules of the game are being respected.
    """
    def test_board_is_empty_by_default(self):
        game = Board()
        self.assertTrue(all(cell is EMPTY for cell in game.cells))

    def test_board_requires_first_player_when_setting_initial_state(self):
        with self.assertRaises(ex.FirstPlayerRequiredError):
            Board([EMPTY, ] * 9)

    def test_board_must_have_nine_cells(self):
        for count in range(0, 8):
            with self.assertRaises(ex.SizeError):
                Board([EMPTY, ] * count, first_player=NAUGHT)

    def test_board_raises_when_marking_a_non_empty_cell(self):
        game = Board()
        game[0] = NAUGHT

        with self.assertRaises(ex.NonEmptyCellError):
            game[0] = CROSS

    def test_game_wont_allow_two_moves_in_a_row_from_either_player(self):
        game = Board()
        game[0] = CROSS
        with self.assertRaises(ex.DoubleMoveError):
            game[1] = CROSS

        game[1] = NAUGHT
        with self.assertRaises(ex.DoubleMoveError):
            game[2] = NAUGHT

    def test_game_knows_when_cross_wins(self):
        game = Board([x, _, o,
                      x, o, x,
                      _, o, _],
                     first_player=x)
        with self.assertRaises(ex.GameOver) as ctx:
            game[6] = x

        self.assertEqual(game.winner, x)
        self.assertEqual(ctx.exception.winner, x)

    def test_game_knows_when_naught_wins(self):
        game = Board([o, _, x,
                      o, x, o,
                      _, x, _],
                     first_player=o)
        with self.assertRaises(ex.GameOver) as ctx:
            game[6] = o

        self.assertEqual(game.winner, o)
        self.assertEqual(ctx.exception.winner, o)

    def test_game_knows_when_there_is_a_draw(self):
        game = Board([o, x, _,
                      x, x, o,
                      o, o, x],
                     first_player=x)
        with self.assertRaises(ex.GameOver) as ctx:
            game[2] = x

        self.assertEqual(game.winner, None)
        self.assertEqual(ctx.exception.winner, None)
        self.assertIn('draw', str(ctx.exception).lower())

    def test_game_board_cannot_be_modified_once_it_has_been_won(self):
        game = Board([x, _, o,
                      x, o, x,
                      _, o, _],
                     first_player=x)
        with self.assertRaises(ex.GameOver):
            game[6] = x

        with self.assertRaises(ex.GameOver):
            # this change should be rolled back
            game[8] = o

        self.assertEqual(game[8], EMPTY)


class NaughtBotTests(unittest.TestCase):
    """
    Tests demonstrating naught_bot's decision-making process.
    """
    def test_knows_how_to_open_first(self):
        game = Board()
        self.assertEqual(naught_bot(game), 4)

    def test_knows_when_to_block(self):
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
        game = Board([o, _, x,
                      _, o, _,
                      x, x, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (8,))

        game = Board([x, o, _,
                      x, o, _,
                      _, _, x],
                     first_player=x)
        self.assertIn(naught_bot(game), (7,))

    def test_prioritize_edge(self):
        """
        This test is for a hole I found during testing. The bot's
        selection process allowed me to win.

        The winning sequence for me was:
        X: 2, 6, 8, 5 <-- X wins (but shouldn't be able to)
        O: 4, 0, 7

        In order to prevent this win, the bot should have selected an edge cell
        during the bot's 2nd move.
        """
        game = Board([_, _, x,
                      _, o, _,
                      x, _, _],
                     first_player=x)
        # by blocking on the edge we can prevent a win for X 2 moves ahead
        self.assertIn(naught_bot(game), (1, 3, 5, 7))
        game = Board([x, _, _,
                      _, o, _,
                      _, _, x],
                     first_player=x)
        self.assertIn(naught_bot(game), (1, 3, 5, 7))

    def test_prioritize_CORRECT_corner(self):
        """
        Another gap found during testing. The bot's
        selection process allowed the player to win.

        The winning sequence for me was:
        X: 0, 7, 6, 3 <-- X wins (but shouldn't be able to)
        O: 4, 2, 8

        In order to prevent this win, the bot should have selected the corner
        opposite the player's first mark (I think).
        """
        game = Board([x, _, _,
                      _, o, _,
                      _, x, _],
                     first_player=x)

        self.assertIn(naught_bot(game), (8, ))

        game = Board([_, _, x,
                      _, o, _,
                      _, x, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (6, ))

        game = Board([_, x, _,
                      _, o, _,
                      _, _, x],
                     first_player=x)
        self.assertIn(naught_bot(game), (0, ))

        game = Board([_, x, _,
                      _, o, _,
                      x, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (2, ))

    def test_block_double_edge_scenario(self):
        """
        This time I'm not sure how to beat the player, but let's work through
        it..

        The winning sequence for me was:
        X: 7, 5, 8, 2 <-- X wins (but shouldn't be able to)
        O: 4, 0, 6

        In order to prevent this win, the bot should have selected the corner
        the corner in between the 2 edges selected in moves 1, and 2.
        """

        game = Board([_, _, _,
                      _, o, x,
                      _, x, _],
                     first_player=x)

        self.assertIn(naught_bot(game), (8, ))

        game = Board([_, _, _,
                      x, o, _,
                      _, x, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (6, ))

        game = Board([_, x, _,
                      x, o, _,
                      _, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (0, ))

        game = Board([_, x, _,
                      _, o, x,
                      _, _, _],
                     first_player=x)
        self.assertIn(naught_bot(game), (2, ))
