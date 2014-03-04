from django.test import TestCase
from tic_tac_toe import TicTacToe

class TestTicTacToe(TestCase):
    def test_has_win_move_along_x(self):
        """
        The player has a winning move along the x axis.
        """
        ttt = TicTacToe(first=False)
        ttt.board = [['O', 'O', None], [None]*3, [None]*3]
        where = ttt.has_win_move()
        assert where == (0, 2)

        ttt = TicTacToe(first=False)
        ttt.board = [[None, 'O', 'O'], [None]*3, [None]*3]
        where = ttt.has_win_move()
        assert where == (0, 0)

    def test_has_win_movie_along_y(self):
        """
        The player has a winning move along the y axis.
        """
        ttt = TicTacToe(first=False)
        ttt.board = [['O', None,  None], ['O', None, None], [None]*3]
        where = ttt.has_win_move()
        assert where == (2, 0)

        ttt = TicTacToe(first=False)
        ttt.board = [[None]*3, ['O', None, None], ['O', None, None]]
        where = ttt.has_win_move()
        assert where == (0, 0)

    def test_has_win_along_diagonals(self):
        """
        A player has a winning move in one of the diagonals.
        """
        ttt = TicTacToe(first=False)
        ttt.board = [['O', None, None], [None, 'O', None], [None]*3]
        where = ttt.has_win_move()
        assert where == (2, 2)

        ttt = TicTacToe(first=False)
        ttt.board = [[None, None, 'O'], [None, 'O', None], [None]*3]
        where = ttt.has_win_move()
        assert where == (2, 0)

        ttt = TicTacToe(first=False)
        ttt.board = [[None]*3, [None, 'O', None], [None, None, 'O']]
        where = ttt.has_win_move()
        assert where == (0, 0)

        ttt = TicTacToe(first=False)
        ttt.board = [[None]*3, [None, 'O', None], ['O', None, None]]
        where = ttt.has_win_move()
        assert where == (0, 2)

    def test_has_fork(self):
        ttt = TicTacToe(first=False)
        ttt.board = [[None, None, None],
                     ['O', 'O', None], 
                     ['O', None, None]]
        where = ttt.has_fork()

    def test_places_match(self):
        ttt = TicTacToe(first=False)
        ttt.board = [[None]*3, [None, 'O', None], [None]*3]
        match = ttt.places_match([(1, 1, 'O')])
        assert match == True

        ttt = TicTacToe(first=False)
        ttt.board = [[None]*3, [None, None, 'O'], [None]*3]
        match = ttt.places_match([(1, 1, 'O')])
        assert match == False



