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
        ttt.board = [['O', None,  None], [None]*3, ['O', None, None]]
        where = ttt.has_win_move()
        assert where == (1, 0)

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
        """
        There is a fork.
        """
        ttt = TicTacToe(first=False)
        ttt.board = [['O', 'X', None],
                     [None, 'O', None],
                     [None, None, 'X']]
        where = ttt.has_fork()
        assert where == (1, 0)
            
    def test_places_match(self):
        """
        Check that the places match algo works.
        """
        ttt = TicTacToe(first=False)
        board = [[None]*3, [None, 'O', None], [None]*3]
        match = ttt.places_match(board, [(1, 1, 'O')])
        assert match == True

        ttt = TicTacToe(first=False)
        board = [[None]*3, [None, None, 'O'], [None]*3]
        match = ttt.places_match(board, [(1, 1, 'O')])
        assert match == False

        ttt = TicTacToe(first=False)
        board = [[None]*3, ['O', None, 'O'], [None]*3]
        match = ttt.places_match(board, [(1, 0, 'O'), (1, 2, 'O')])
        assert match == True

    def test_ai_move_we_win(self):
        ttt = TicTacToe(first=False)
        ttt.board = [['X', None, 'X'], [None]*3, [None]*3]
        ttt.ai_move()
        assert ttt.board[0][1] == 'X'

    def test_ai_move_block_win(self):
        ttt = TicTacToe(xo='O', first=False)
        ttt.board = [['X', None, 'X'], [None]*3, [None]*3]
        ttt.ai_move()
        assert ttt.board[0][1] == 'O'
        
    def test_ai_move_block_opp_fork(self): 
        ttt = TicTacToe(xo='O', first=False)
        ttt.board = [['X', None, None],
                     [None, 'O', None],
                     [None, None, 'X']]
        ttt.ai_move()
        assert ttt.board[0][1] == 'O'
