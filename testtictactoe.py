import model
import strategy
import unittest


class TestEmptyGame(unittest.TestCase):

    def setUp(self):
        model.clear_board()

    def test_clear_board(self):
        board_as_list = [square for row in model.board for square in row]
        self.assertEquals(board_as_list, [None, None, None, None, None, None, None, None, None])

    def test_update_square(self):
        model.update_square(model.X, model.TOP_RIGHT)
        self.assertEqual(model.board[0][2], model.X)

        model.update_square(model.O, model.CENTER)
        self.assertEqual(model.board[1][1], model.O)

    def test_failed_update_square(self):
        model.update_square(model.O, model.CENTER)
        self.assertRaises(model.DoubleMoveError, model.update_square, model.X, model.CENTER)

    def test_build_state(self):
        none_list = [None, None, None]
        self.assertEqual(model.top_row, none_list)
        self.assertEqual(model.middle_row, none_list)
        self.assertEqual(model.bottom_row, none_list)
        self.assertEqual(model.left_column, none_list)
        self.assertEqual(model.middle_column, none_list)
        self.assertEqual(model.right_column, none_list)
        self.assertEqual(model.left_diagonal, none_list)
        self.assertEqual(model.right_diagonal, none_list)

    def test_line_check(self):
        result = (0, 0, 3)
        self.assertEqual(model.line_check(model.top_row, model.X), result)
        self.assertEqual(model.line_check(model.middle_row, model.X), result)
        self.assertEqual(model.line_check(model.bottom_row, model.X), result)
        self.assertEqual(model.line_check(model.left_column, model.X), result)
        self.assertEqual(model.line_check(model.middle_column, model.X), result)
        self.assertEqual(model.line_check(model.right_column, model.X), result)
        self.assertEqual(model.line_check(model.left_diagonal, model.X), result)
        self.assertEqual(model.line_check(model.right_diagonal, model.X), result)

    def test_can_player_win(self):
        self.assertEqual(model.can_player_win(model.X), None)
        self.assertEqual(model.can_player_win(model.O), None)

    def test_can_player_fork(self):
        self.assertEqual(model.can_player_fork(model.X), False)

    def test_is_board_empty(self):
        self.assertEqual(model.is_board_empty(), True)

    def test_is_center_empty(self):
        self.assertEqual(model.is_center_empty(), True)

    def test_is_corner_empty(self):
        test_array = [model.TOP_LEFT, model.TOP_RIGHT, model.BOT_LEFT, model.BOT_RIGHT]
        self.assertEqual(model.is_corner_empty(), test_array)

    def test_empty_sides(self):
        test_array = [model.TOP_MID, model.MID_LEFT, model.MID_RIGHT, model.BOT_MID]
        self.assertEqual(model.empty_sides(), test_array)

    def test_did_player_win(self):
        self.assertEqual(model.did_player_win(model.X), False)

    def test_pick_move(self):
        self.assertIn(strategy.pick_move(), [model.TOP_LEFT, model.TOP_RIGHT, model.BOT_LEFT, model.BOT_RIGHT])


class TestMidGame(unittest.TestCase):

    def setUp(self):
        model.clear_board()
        model.update_square(model.X, (0, 0))
        model.update_square(model.O, (1, 1))
        model.update_square(model.X, (2, 2))

    def test_clear_board(self):
        model.clear_board()
        board_as_list = [square for row in model.board for square in row]
        self.assertEquals(board_as_list, [None, None, None, None, None, None, None, None, None])

    def test_update_square(self):
        model.update_square(model.O, (1, 2))
        self.assertEqual(model.board[1][2], model.O)
        self.assertRaises(model.DoubleMoveError, model.update_square, model.X, (1, 1))

    def test_build_state(self):
        self.assertEqual(model.top_row, [1, None, None])
        self.assertEqual(model.middle_row, [None, 2, None])
        self.assertEqual(model.bottom_row, [None, None, 1])
        self.assertEqual(model.left_column, [1, None, None])
        self.assertEqual(model.middle_column, [None, 2, None])
        self.assertEqual(model.right_column, [None, None, 1])
        self.assertEqual(model.left_diagonal, [1, 2, 1])
        self.assertEqual(model.right_diagonal, [None, 2, None])

    def test_line_check(self):
        self.assertEqual(model.line_check(model.top_row, model.X), (1, 0, 2))
        self.assertEqual(model.line_check(model.middle_row, model.X), (0, 1, 2))
        self.assertEqual(model.line_check(model.bottom_row, model.X), (1, 0, 2))
        self.assertEqual(model.line_check(model.left_column, model.X), (1, 0, 2))
        self.assertEqual(model.line_check(model.middle_column, model.X), (0, 1, 2))
        self.assertEqual(model.line_check(model.right_column, model.X), (1, 0, 2))
        self.assertEqual(model.line_check(model.left_diagonal, model.X), (2, 1, 0))
        self.assertEqual(model.line_check(model.right_diagonal, model.X), (0, 1, 2))

    def test_can_player_win(self):
        self.assertEqual(model.can_player_win(model.X), None)
        self.assertEqual(model.can_player_win(model.O), None)

    def test_can_player_fork(self):
        self.assertEqual(model.can_player_fork(model.X), True)

    def test_is_board_empty(self):
        self.assertEqual(model.is_board_empty(), False)

    def test_is_corner_empty(self):
        test_array = [model.TOP_RIGHT, model.BOT_LEFT]
        self.assertEqual(model.is_corner_empty(), test_array)

    def test_empty_sides(self):
        test_array = [model.TOP_MID, model.MID_LEFT, model.MID_RIGHT, model.BOT_MID]
        self.assertEqual(model.empty_sides(), test_array)

    def test_did_player_win(self):
        self.assertEqual(model.did_player_win(model.X), False)

    def test_pick_move(self):
        strategy.computer_flag = model.O
        strategy.player_flag = model.X
        self.assertIn(strategy.pick_move(), [model.TOP_MID, model.MID_LEFT, model.MID_RIGHT, model.BOT_MID])
        strategy.computer_flag, strategy.player_flag = strategy.player_flag, strategy.computer_flag
        model.update_square(model.O, (1, 2))
        self.assertEqual(strategy.pick_move(), (1, 0))


if __name__ == '__main__':
    unittest.main()