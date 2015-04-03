import random
from django.test import TestCase

from game.models import Game


class GameModelTest(TestCase):
    def test_play_first(self):
        "X always goes first"

        game = Game()
        game.play(0)
        self.assertEqual(game.board, "X        ")
        self.assertEqual(game.next_player, "O")

    def test_play_second(self):
        "The second play is O"

        game = Game(board="X        ")
        game.play(1)
        self.assertEqual(game.board, "XO       ")
        self.assertEqual(game.next_player, "X")

    def test_play_error_square_taken(self):
        "You can't play a square that is taken."

        game = Game(board="XOX      ")
        with self.assertRaises(ValueError):
            game.play(1)
            game.play(2)

    def test_play_error_index(self):
        "You can't pass in an invalid index."

        game = Game()
        with self.assertRaises(IndexError):
            game.play(-1)
            game.play(9)
            game.play(10)

    def test_play_auto_human_computer(self):
        "At the start of the game, human starts."
        game = Game(player_x='human', player_o='game.players.RandomPlayer')
        game.play_auto()
        self.assertEqual(game.board, "         ")
        self.assertEqual(game.next_player, "X")

    def test_play_auto_computer_human(self):
        "At the start of the game, computer starts."
        random.seed(0)
        game = Game(player_o='human', player_x='game.players.RandomPlayer')
        game.play_auto()
        self.assertEqual(game.board, "       X ")
        self.assertEqual(game.next_player, "O")

    def test_play_auto_computer_to_computer(self):
        "Two computers playing against themselves."
        random.seed(0)
        game = Game(player_o='game.players.RandomPlayer', player_x='game.players.RandomPlayer')
        game.play_auto()
        self.assertEqual(game.board, "OOXOX OXX")
        self.assertEqual(game.is_game_over, 'O')

    def test_game_over(self):
        "Runs through a bunch of board states, with the expected result."

        states = [
            ("         ", None),  # Initial state
            ("X        ", None),  # First play
            ("X       O", None),  # Second play
            ("XXXOO    ", 'X'),   # Easy X win (across top)
            ("OOOXX  X ", 'O'),   # Easy O win (across top)
            ("XOO X   X", 'X'),   # Easy X win (diagonal)
            ("XXO O O X", 'O'),   # Easy O win (diagonal)
            ("XOXXOXOXO", ' '),   # Stalemate
        ]
        for state in states:
            game = Game(board=state[0])
            self.assertEqual(game.is_game_over, state[1],
                             "is_game_over='{0}' for board='{1}', expected='{2}'".format(game.is_game_over,
                                                                                         game.board, state[1]))
