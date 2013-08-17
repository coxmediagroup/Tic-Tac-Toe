from nose.tools import assert_equal
#from mock import Mock


from ttt.tictactoe import checkForWin


class TestCheckForWin():
    def setUp(self):
        self.board = []

    def test_checkForWin_row_win(self):
        board = [1, 1, 1,
                 1, 0, 1,
                 0, 1, 0]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_row_1_lose(self):
        board = [1, 1, None,
                 1, 0, 1,
                 0, 1, 0]
        assert_equal(False, checkForWin(board))

    def test_checkForWin_last_row_win(self):
        board = [0, 1, 0,
                 1, 0, 1,
                 1, 1, 1]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_column_win(self):
        board = [1, 0, 0,
                 1, 0, 1,
                 1, 1, 0]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_last_column_win(self):
        board = [1, 0, 0,
                 1, 1, 0,
                 0, 1, 0]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_diagonal_win(self):
        board = [1, 0, 1,
                 0, 1, 0,
                 0, 1, 1]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_diagonal_loose(self):
        board = [None, 1, 1,
                 None, None, None,
                 None, None, None]
        # This is a condition seen while playing
        #that was due to a variable being reused
        #when a value should have been hard coded.
        assert_equal(False, checkForWin(board))

    def test_checkForWin_diagonal_win_other_diag(self):
        board = [1, 0, 0,
                 0, 0, 0,
                 0, 1, 1]
        assert_equal(True, checkForWin(board))

    def test_checkForWin_false_because_of_tie(self):
        board = [1, 0, 1,
                 0, 1, 0,
                 0, 1, 0]
        assert_equal(False, checkForWin(board))
