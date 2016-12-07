
import unittest
import itertools
from ttt.board import board
from ttt.player import player
import game


class GameTests(unittest.TestCase):

    @staticmethod
    def create_board(o_squares, x_squares):
        b = board.Board(9)
        [b.place(i, "O") for i in o_squares]
        [b.place(i, "X") for i in x_squares]
        return b

    @staticmethod
    def combos(size):
        items = list(itertools.combinations(range(9), size))
        lists = [list(i) for i in items]
        return lists

    def test_check_for_winner_singles(self):
        g = game.AbstractGame(None, None)
        for i in GameTests.combos(1):
            g.board = GameTests.create_board(i, [])
            self.assertIsNone(g.check_for_winner(), i)

    def test_check_for_winner_doubles(self):
        g = game.AbstractGame(None, None)
        for i in GameTests.combos(2):
            g.board = GameTests.create_board(i, [])
            self.assertIsNone(g.check_for_winner(), i)

    def test_check_for_winner_triples(self):
        player1 = player.ComputerPlayer("X")
        player2 = player.ComputerPlayer("O")
        g = game.AbstractGame(player1, player2)

        winners = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for test in GameTests.combos(3):
            g.winner = None
            g.board = GameTests.create_board(test, [])

            if test in winners:
                self.assertEqual(player2, g.check_for_winner(), test)
            else:
                self.assertIsNone(g.check_for_winner(), test)
