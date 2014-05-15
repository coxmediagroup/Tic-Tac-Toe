"""
Tests for the Tic-Tac-Toe console game.
"""
from board import Board
from errors import TicTacToeError
from mock import patch
from unittest.case import TestCase
import errorcodes
import ttt


class TestTicTacToe(TestCase):
    """
    Tests for the Tic-Tac-Toe console game.
    """

    @staticmethod
    def get_printed_boards(mock_stdout):
        """
        Get the list of boards printed out to the console during the scope of C{mock_stdout}.

        @param mock_stdout: The L{mock.MagicMock} for mocking out print statements during the test
        @type mock_stdout: L{mock.MagicMock}
        @return: The list of Tic-Tac-Toe boards printed out while C{mock_stdout} was active
        @rtype: list [str]
        """
        printed_boards = []
        for mock_call in mock_stdout.write.mock_calls:
            print_output = (mock_call[1] or ("",))[0]
            if print_output.count("-|-") >= 4:
                printed_boards.append(print_output)
        return printed_boards

    def test_creating_board(self):
        """
        Test that the tic-tac-toe board has no X or O positions upon creation.
        """
        board = Board()
        self.assertEquals(board.x_positions, set())
        self.assertEquals(board.o_positions, set())

    def test_gameplay_first_player_first_move(self):
        """
        Test initial gameplay logic and/or AI when going first
        """
        board = Board()
        first_move = board.find_next_move('X')
        self.assertIn(first_move, board.CORNERS)

    def test_gameplay_first_player_second_move(self):
        """
        Test that second play as AI makes sense (assuming AI was the first player)
        """
        board = Board()
        board.add_mark(0, "X")
        pos_move_dict = {1: [2, 6], 8: [2, 6], 2: [8]}
        for pos, expected_moves in pos_move_dict.iteritems():
            board.o_positions.clear()
            board.add_mark(pos, "O")
            second_move = board.find_next_move("X")
            self.assertIn(second_move, expected_moves)

    def test_gameplay_second_player(self):
        """
        Test that the AI picks the middle square as quickly as possible when playing second
        """
        board = Board()
        board.add_mark(0, "O")
        self.assertEquals(4, board.find_next_move("X"))

    def test_gameplay_winning_blocking(self):
        """
        Test that if a player can win in one move, it becomes both the player and opponent's next move
        """
        board = Board()
        board.add_mark(0, "O")
        board.add_mark(3, "O")
        board.add_mark(1, "X")
        self.assertEquals(6, board.find_next_move("O"))  # Test winning move is made by O if left open
        self.assertEquals(6, board.find_next_move("X"))  # Test winning move is blocked by X

    def test_gameplay_first_player_winning_setup(self):
        """
        Test that the first player will have a winning setup if the middle square is left unplayed.
        """
        board = Board()
        board.add_mark(0, "O")
        board.add_mark(1, "X")
        board.add_mark(6, "O")
        board.add_mark(board.find_next_move("X"), "X")
        self.assertIn(board.find_next_move("O"), [4, 8])  # 4 and 8 guarantee the win for O

        board.add_mark(4, "O")
        board.add_mark(board.find_next_move("X"), "X")
        board.add_mark(board.find_next_move("O"), "O")
        self.assertEquals(board.get_winner(), "O")  # Test that O actually wins the game

    def test_gameplay_identical_opposite_mark(self):
        """
        Test that the gameplay followed in the above test is identical when the symbols are reversed
        """
        board = Board()
        board.add_mark(0, "X")
        board.add_mark(1, "O")
        board.add_mark(6, "X")
        board.add_mark(board.find_next_move("O"), "O")
        self.assertIn(board.find_next_move("X"), [4, 8])  # 4 and 8 guarantee the win for X

        board.add_mark(4, "X")
        board.add_mark(board.find_next_move("O"), "O")
        board.add_mark(board.find_next_move("X"), "X")
        self.assertEquals(board.get_winner(), "X")  # Test that X actually wins the game

    @patch("sys.stdout")
    def test_print_board_in_play(self, mock_stdout):
        """
        Test printing the game board when in play
        """
        board = Board()
        board.add_mark(0, "X")
        board.add_mark(6, "O")
        board.add_mark(1, "X")
        board.add_mark(7, "O")
        board.print_board()
        printed_text = self.get_printed_boards(mock_stdout)[0]
        self.assertNotIn("Winner", printed_text)
        self.assertEquals(printed_text.count("X"), 2)
        self.assertEquals(printed_text.count("O"), 2)

    @patch("sys.stdout")
    def test_print_board_with_winner(self, mock_stdout):
        """
        Test printing the game board after a winner has been determined.
        """
        board = Board()
        board.add_mark(0, "X")
        board.add_mark(6, "O")
        board.add_mark(1, "X")
        board.add_mark(7, "O")
        board.add_mark(2, "X")
        board.print_board()
        printed_text = self.get_printed_boards(mock_stdout)[0]
        self.assertIn("Winner", printed_text)
        self.assertEquals(printed_text.count("X"), 4)
        self.assertEquals(printed_text.count("O"), 2)

    def test_add_mark_already_selected(self):
        """
        Test adding a mark to an already-selected position results in an error
        """
        board = Board()
        board.add_mark(0, "X")
        self.assertRaises(TicTacToeError, board.add_mark, 0, "O")

    def test_operating_completed_game(self):
        """
        Test that finding a move or adding a mark on a completed board results in an error
        """
        board = Board()
        board.add_mark(0, "X")
        board.add_mark(1, "O")
        board.add_mark(4, "X")
        board.add_mark(7, "O")
        board.add_mark(8, "X")  # X has Tic-Tac-Toe on the diagonal
        self.assertRaises(TicTacToeError, board.find_next_move, "O")
        self.assertRaises(TicTacToeError, board.add_mark, 2, "O")

    def test_error_as_string(self):
        """
        Test formatting of a TicTacToeError object
        """
        error = TicTacToeError("Test", errorcodes.NO_POSITIONS_AVAILABLE)
        expected_str = "[NO_POSITIONS_AVAILABLE] Test"
        self.assertEquals(str(error), expected_str)
        self.assertEquals(repr(error), expected_str)

    @patch("sys.stdout")
    @patch("sys.stdin")
    def test_main_single_duplicate_turn(self, mock_stdin, mock_stdout):
        """
        Test running the game and taking one turn, and then duplicating it
        """
        commands = ["n", "4", "4", "p", "z", "q"]
        mock_stdin.readline.side_effect = lambda *args, **kw: commands.pop(0)
        ttt.main()
        printed_boards = self.get_printed_boards(mock_stdout)
        self.assertEquals(printed_boards[0].count("O"), 1)  # Only one turn taken -> only one O

    @patch("sys.stdin")
    @patch("ttt.is_user_first")
    @patch("board.Board.is_playable", False)
    @patch("board.Board.add_mark")
    def test_take_turn_computer_playable(self, mock_add_mark, mock_is_user_first, mock_stdin):
        """
        Test that the computer takes a turn only when the board is actually playable
        """
        mock_is_user_first.return_value = True
        commands = ["n", "4", "q"]
        mock_stdin.readline.side_effect = lambda *args, **kw: commands.pop(0)
        ttt.main()
        self.assertEquals(mock_add_mark.call_count, 1)

    @patch("sys.stdout")
    @patch("sys.stdin")
    @patch("ttt.is_user_first")
    def test_main_randomizes_first_player(self, mock_is_user_first, mock_stdin, mock_stdout):
        """
        Test that each new game randomizes the first player
        """
        commands = ["n", "p", "n", "p", "q"]
        mock_stdin.readline.side_effect = lambda *args, **kw: commands.pop(0)
        mock_is_user_first.side_effect = lambda *args, **kw: commands.count("p") < 2
        ttt.main()
        printed_boards = self.get_printed_boards(mock_stdout)
        self.assertIn("X", printed_boards[0])
        self.assertNotIn("X", printed_boards[1])

    @patch("random.randrange")
    def test_is_user_first(self, mock_randrange):
        """
        Test that the order of play depends on the output of random.randrange
        """
        rand_outputs = [3, 3, 5, 6, 2, 1]  # Dice are tied, then computer is first, then user is first.
        mock_randrange.side_effect = lambda *args, **kw: rand_outputs.pop(0)
        self.assertFalse(ttt.is_user_first())
        self.assertTrue(ttt.is_user_first())
