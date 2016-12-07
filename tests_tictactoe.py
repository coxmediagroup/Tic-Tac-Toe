from random import choice
import unittest

from tictactoe import Board, Player, Minimax


class TestTicTacToe(unittest.TestCase):

    def test_board_print_as_grid(self):
        """
        Tests that board is printed as a grid.
        """
        board = Board()
        board_grid_str = """
        |0|1|2|
        |3|4|5|
        |6|7|8|
        """
        self.assertEqual(board_grid_str, board.__str__())

    def test_board_get_win_detection(self):
        """
        Tests that a board can detect when a win is present.
        """
        board = Board()
        self.assertFalse(board.get_win())

        # create a player and mark a winning move
        player = Player(board, 'H', 'human')
        winning_move = choice(board.WINNING_POSITIONS)
        for space in winning_move:
            board.spaces[space] = player
        self.assertTrue(board.get_win())
       
    def test_minimax(self):
        """
        Tests that computer can block human. 
        """
        board = Board()
        computer = Player(board, 'C', 'computer', is_human=False, ai_strat=Minimax(board))
        human = Player(board, 'H', 'human')
        # set up human about to win
        board.spaces[0] = human
        board.spaces[1] = human
        # set up computer to not have win cond
        board.spaces[4] = computer
        board.spaces[8] = computer
        """
        |H|H|2|
        |3|C|5|
        |6|7|C|
        """
        board.CURRENT_PLAYER = computer
        board.WAITING_PLAYER = human 

        self.assertEqual(2, computer.make_play())

    def test_minimax_failing_block(self):
        """
        |H|1|H|
        |3|C|5|
        |6|7|8|
        """
        board = Board()
        computer = Player(board, 'C', 'computer', is_human=False, ai_strat=Minimax(board))
        computer.ai_strat.MINIMAX_DEPTH = 1
        human = Player(board, 'H', 'human')
        board.spaces[0] = human
        board.spaces[2] = human
        board.spaces[4] = computer
        board.CURRENT_PLAYER = computer
        board.WAITING_PLAYER = human 
        self.assertEqual(1, computer.make_play())
