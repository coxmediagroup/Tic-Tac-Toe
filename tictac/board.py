"""
    Tic Tac Toe game represented in Python.

    Based on https://github.com/coxmediagroup/Tic-Tac-Toe

    Board Representation
    - 9 character string
    - Blank spaces represented by -
    - x and o used for their player pieces respectively
    - relative positions as follows:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    _________
    6 | 7 | 8

    Example:

    X | O | 
    ---------
    X | X | O
    ---------
    O |   | 

    is represented by 'xo-xxoo--'
    
"""

import re

class TTTGameBoard(object):

    # Lines of victory on the board, given above numbering
    lines = [
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,4,8),
        (2,4,6)
    ]

    def __init__(self, board='---------', active_player='x', last_move=None):
        board = board.lower()
        board_test = re.compile('^'+'[xo-]'*9+'$')
        if board and not board_test.match(board):
            raise ValueError("Invalid board format.")

        active_player = active_player.lower()
        if active_player != 'x' and active_player != 'o':
            raise ValueError("Active player must be x or o.")

        self.board = board
        self.active_player = active_player
        self.last_move = last_move
        self.winner = self.get_winner()
        self.depth = 9 - len(self.get_legal_moves())

    def __repr__(self):
        return "TTTGameBoard [{}] W:{} P:{} LM:{} D:{}".format(
            self.board, 
            self.winner, 
            self.active_player, 
            self.last_move, 
            self.depth
        )


    # return a (fixed-width) test friendly board representation
    def friendly_board(self):
        return self.board[0:3] + '\n' + self.board[3:6] + '\n' + self.board[6:9]


    # get the winner of the current board state.
    # if there is no winner, return None
    # in the case of invalid board states with 2 winners, x takes priority
    def get_winner(self):
        current_lines = [ ''.join([ self.board[p] for p in line ]) for line in self.lines ]
        if 'xxx' in current_lines:
            return 'x'
        elif 'ooo' in current_lines:
            return 'o'
        else:
            return None


    # return a list of legal moves
    def get_legal_moves(self):
        return [ i for i, c in enumerate(self.board) if c == '-' ]


    # return a new TTTGameBoard object with the new board state
    def apply_move(self, point):
        if point not in self.get_legal_moves():
            raise ValueError("Invalid move.")
        board_list = list(self.board)
        board_list[point] = self.active_player
        other_player = 'x' if self.active_player == 'o' else 'o'
        return TTTGameBoard(''.join(board_list), active_player=other_player, last_move=point)
