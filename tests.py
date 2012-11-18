import unittest

from players import ComputerPlayerO, WINNING_MOVES, CORNERS, CADDY_CORNERS, \
    CADDY_CORNER_MAP, CORNER_BORDERS_MAP


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

    def test_creation(self):
        board = get_board(xes=[0])
        player = ComputerPlayerO(board)
        self.assertEqual(player.xes, [0])

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

    def test_round_one(self):
        # take center if X takes a corner
        board = get_board(xes=[0])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertEqual(next_move, 4)
        # if X takes center, pick a random corner
        board = get_board(xes=[4])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertTrue(next_move in CORNERS)

    def test_round_two_strategy_one(self):
        # If X threatens a win, block it
        board = get_board(xes=[0, 2], oes=[4])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertEqual(next_move, 1)

    def test_round_two_strategy_two(self):
        # If the X's are caddy corner, play 3, 5 or 7 to force a tie
        for corner_set in CADDY_CORNERS:
            board = get_board(xes=corner_set, oes=[4])
            player = ComputerPlayerO(board)
            next_move = player.play()
            self.assertTrue(next_move in [3, 5, 7])

    def test_round_two_strategy_three(self):
        # If X on edge and corner, play the corner square caddy-corner
        # to the corner X
        for k, v in CADDY_CORNER_MAP.items():
            # make sure we're providing a wall square that
            # doesn't threaten a win
            other_x = 1
            if k in [0, 2]:
                other_x = 7
            board = get_board(xes=[other_x, k], oes=[4])
            player = ComputerPlayerO(board)
            next_move = player.play()
            self.assertEqual(next_move, v)

    def test_round_two_strategy_four(self):
        # If X's border a corner, play in that corner
        for x_set, o in CORNER_BORDERS_MAP.items():
            board = get_board(xes=list(x_set), oes=[4])
            player = ComputerPlayerO(board)
            next_move = player.play()
            self.assertEqual(next_move, o)

    def test_round_two_strategy_five(self):
        # Else, pick a remaining corner
        board = get_board(xes=[0, 5], oes=[4])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertTrue(next_move in [2, 6, 8])

    def test_round_three_take_the_win(self):
        board = get_board(xes=[3, 5, 7], oes=[2, 4])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertEqual(next_move, 6)

    def test_round_three_blocks_the_win(self):
        board = get_board(xes=[0, 6, 7], oes=[4, 8])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertEqual(next_move, 3)

    def test_game_over_with_win(self):
        board = get_board(xes=[3, 5, 7], oes=[2, 4])
        player = ComputerPlayerO(board)
        next_move = player.play()
        self.assertEqual(next_move, 6)
        game_over, winning_squares = player.is_game_over()
        self.assertTrue(game_over)
        self.assertEqual(winning_squares, [2, 4, 6])

    def test_tie_game(self):
        board = get_board(xes=[0, 2, 5, 6, 7], oes=[1, 3, 4, 8])
        player = ComputerPlayerO(board)
        game_over, winning_squares = player.is_game_over()
        self.assertTrue(game_over)
        self.assertFalse(winning_squares)


if __name__ == "__main__":
    unittest.main()
