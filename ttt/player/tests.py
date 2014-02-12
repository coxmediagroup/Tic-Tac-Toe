
import unittest
from ttt.board import board
import player


class PlayerTests(unittest.TestCase):

    def test_player_first_move(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")

        i = p.get_square(b, "")

        self.assertEqual(4, i, "PC first move")

    def test_player_range(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")
        valid_moves = range(0, 9)

        while not b.is_full():
            i = p.get_square(b, "")
            self.assertTrue(i in valid_moves, "Invalid Move: %d" % i)
            b.place(i, p.marker)
