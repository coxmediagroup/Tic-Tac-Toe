
import unittest
from ttt.board import board
import player


class PlayerTests(unittest.TestCase):

    def test_check_for_block(self):
        cases = [
            ([0, 1], 2),
            ([3, 4], 5),
            ([6, 7], 8),
            ([0, 3], 6),
            ([1, 4], 7),
            ([2, 5], 8),
            ([0, 4], 8),
            ([2, 4], 6),
        ]

        for x_values, rtn in cases:
            b = board.Board(9)
            p = player.ComputerPlayer("O")
            for x in x_values:
                b.place(x, "X")
            i = p.check_for_block(b)
            self.assertEqual(rtn, i, "For %s, expected %s; got %s" % (x_values,
                                                                      rtn,
                                                                      i))

    def test_check_for_win(self):
        cases = [
            ([0, 1], 2),
            ([3, 4], 5),
            ([6, 7], 8),
            ([0, 3], 6),
            ([1, 4], 7),
            ([2, 5], 8),
            ([0, 4], 8),
            ([2, 4], 6),
        ]

        for x_values, rtn in cases:
            b = board.Board(9)
            p = player.ComputerPlayer("X")
            for x in x_values:
                b.place(x, "X")
            i = p.check_for_win(b)
            self.assertEqual(rtn, i, "For %s, expected %s; got %s" % (x_values,
                                                                      rtn,
                                                                      i))

    def test_player_first_move(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")

        i = p.get_square(b, None, "")

        self.assertEqual(4, i, "PC first move, first player")

    def test_player_range(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")
        valid_moves = range(0, 9)
        prev = None

        while not b.is_full():
            i = p.get_square(b, prev, "")
            self.assertTrue(i in valid_moves, "Invalid Move: %d" % i)
            b.place(i, p.marker)
            prev = i

    def test_second_player_first_move_1(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")

        i = p.get_square(b, 4, "")

        self.assertEqual(6, i, "PC first move, second player")

    def test_second_player_first_move_2(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")

        i = p.get_square(b, 0, "")

        self.assertEqual(4, i, "PC first move, second player")

    def test_odd_case(self):
        b = board.Board(9)
        p = player.ComputerPlayer("X")

        b.place(4, "O")
        i = p.get_square(b, 4, "")
        self.assertEqual(6, i, "PC first move, second player")
        b.place(i, "X")

        b.place(2, "O")
        i = p.get_square(b, 2, "")
        self.assertEqual(0, i, "PC move when User doing first_player()")
        b.place(i, "X")

        b.place(3, "O")
        i = p.get_square(b, 3, "")
        self.assertEqual(5, i, "Should be 5 for block, got %d" % i)
        b.place(i, "X")
