import unittest

from players import ComputerPlayerO, WINNING_MOVES


def get_board(xes=[], oes=[]):
    board = [{"has_x": False, "has_o": False} for x in range(9)]
    for x in xes:
        board[x]["has_x"] = True
    for o in oes:
        board[o]["has_o"] = True
    return board


class ComputerPlayerOTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_blocks_all_threatened_wins(self):
        """tests if the player will give the correct move to block any
        winning combination.
        """
        for win in WINNING_MOVES:
            board = get_board(xes=win[0:2])
            player = ComputerPlayerO(board)
            next_move = player.play()
            self.assertEqual(next_move, win[2])

    def test_takes_the_win(self):
        """tests if the player will take any possible winning combination
        if given the chance.
        """
        for win in WINNING_MOVES:
            board = get_board(oes=win[0:2])
            player = ComputerPlayerO(board)
            next_move = player.play()
            self.assertEqual(next_move, win[2])


if __name__ == "__main__":
    unittest.main()
