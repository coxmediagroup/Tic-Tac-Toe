import model
import unittest

class TestModelFunctions1(unittest.TestCase):

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
        self.assertRaises(Exception, model.update_square,(model.X, model.CENTER))


if __name__ == '__main__':
    unittest.main()