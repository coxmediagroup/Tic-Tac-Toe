
import copy

class TicTacToe(object):
    """
    TicTacToe simulates a player and should never lose a game of TicTacToe. The assumption
    for the game is that X goes first and O goes second.
    """
    def __init__(self, side):
        if side not in ('X', 'O'):
            raise ValueError("side is invalid. Must be either X, O.")
        self.is_x = True if side == 'X' else False

    def _validate_board(self, board):
        """
        Validates the board state and raises an Exception if it is invalid.
        """
        num_x, num_o = 0, 0
        for i in xrange(3):
            for j in xrange(3):
                # IndexErrors may occur if the board is not 3x3
                if board[i][j] == 'X':
                    num_x += 1
                elif board[i][j] == 'O':
                    num_o += 1
                elif board[i][j] != ' ':
                    raise ValueError("Invalid board state. Only ' ', X, O are allowed in cells")
        if self.is_x:
            if num_x != num_o:
                raise ValueError("Invalid board state. On Xs turn, each side should have same # of choices")
        else:
            if num_x - 1 != num_o:
                raise ValueError("Invalid board state. On Os turn, X should have made 1 more choice")

    def _max(self, board, turn, prev_min=100, prev_max=-100):
        """
        MinMax algorithm where the following values are given to various board states:
        Win = 1, Lose = -1, Tie = 0
        """
        max_value, max_row, max_col = -100, None, None
        for i in xrange(3):
            for j in xrange(3):
                if board[i][j] == ' ':
                    value, row, col = None, None, None
                    board[i][j] = 'X' if turn == 'X' else 'O'
                    winner = self.winner(board)
                    if winner:
                        if winner == 'X':
                            if self.is_x:
                                value, row, col = 1, i, j
                            else:
                                value, row, col = -1, i, j
                        elif winner == 'O':
                            if self.is_x:
                                value, row, col = -1, i, j
                            else:
                                value, row, col = 1, i, j
                        else:
                            value, row, col = 0, i, j
                    else:
                        next_turn = 'O' if turn == 'X' else 'X'
                        value, row, col = self._min(board, next_turn, prev_min, prev_max)
                    board[i][j] = ' '
                    if value > prev_min:
                        return value, i, j
                    if value > prev_max:
                        prev_max = value
                    if value > max_value:
                        max_value = value
                        max_row, max_col = i, j
        return max_value, max_row, max_col

    def _min(self, board, turn, prev_min=1, prev_max=-1):
        """
        MinMax algorithm where the following values are given to various board states:
        Win = 1, Lose = -1, Tie = 0
        """
        min_value, min_row, min_col = 100, None, None
        for i in xrange(3):
            for j in xrange(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X' if turn == 'X' else 'O'
                    winner = self.winner(board)
                    if winner:
                        if winner == 'X':
                            if self.is_x:
                                value, row, col = 1, i, j
                            else:
                                value, row, col = -1, i, j
                        elif winner == 'O':
                            if self.is_x:
                                value, row, col = -1, i, j
                            else:
                                value, row, col = 1, i, j
                        else:
                            value, row, col = 0, i, j
                    else:
                        next_turn = 'O' if turn == 'X' else 'X'
                        value, row, col = self._max(board, next_turn, prev_min, prev_max)
                    board[i][j] = ' '
                    if value < prev_max:
                        return value, i, j
                    if value < prev_min:
                        prev_min = value
                    if value < min_value:
                        min_value = value
                        min_row, min_col = i, j
        return min_value, min_row, min_col

    def winner(self, board):
        """
        Returns 'X' if X has won, 'O' if O has won, and ' ' if the game has ended in a tie.
        If the game has not yet completed, returns None.
        """
        # Check rows
        total_choices = 0
        for i in xrange(3):
            num_x, num_o = 0, 0
            for j in xrange(3):
                if board[i][j] == 'X':
                    num_x += 1
                elif board[i][j] == 'O':
                    num_o += 1
            if num_x == 3:
                return 'X'
            elif num_o == 3:
                return 'O'
            total_choices += num_x + num_o
        # Check cols
        for j in xrange(3):
            num_x, num_o = 0, 0
            for i in xrange(3):
                if board[i][j] == 'X':
                    num_x += 1
                elif board[i][j] == 'O':
                    num_o += 1
            if num_x == 3:
                return 'X'
            elif num_o == 3:
                return 'O'
        # Check diagonals
        if board[1][1] != ' ':
            if board[0][0] == board[1][1] and board[2][2] == board[1][1]:
                return board[1][1]
            if board[0][2] == board[1][1] and board[2][0] == board[1][1]:
                return board[1][1]
        # Since there are no winners, if the board is full (9 choices made) then its a tie
        if total_choices == 9:
            return ' '
        else:
            return None

    def make_move(self, board):
        self._validate_board(board)
        updated_board = copy.deepcopy(board)
        winner = self.winner(updated_board)
        if winner:
            return updated_board
        side = 'X' if self.is_x else 'O'
        score, row, col = self._max(updated_board, side)
        updated_board[row][col] = side
        return updated_board
