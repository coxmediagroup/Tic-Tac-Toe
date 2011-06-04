"""
Tic-Tac-Toe game logic

This is the game logic for Tic-Tac-Toe that allows a computer player
to always win or draw a game. In keeping with the spirit of the Zen of
Python, the logic is kept fairly simple instead of using complex techniques
such as minimax algorithms and decision trees.
"""
from random import choice

__author__ = "Nick Schwane"

CORNERS = [0, 2, 6, 8]
EDGES = [1, 3, 5, 7]
CENTER = 4
WINNERS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
EMPTY = ' '


def check_for_win(board, mark):
    """
    Check to see if there is a winning condition for the specified mark
    """    
    for winner in WINNERS:
        if board[winner[0]] == mark and board[winner[1]] == mark and board[winner[2]] == mark:
            return True
    return False


def construct_board(request):
    """
    Construct game board from request object
    """
    board = []
    for i in range(0, 9):
        board.append(request.GET.get(str(i), EMPTY))
    mark = request.GET.get('mark')
    return board, mark


def determine_computer_move(board, mark):
    """
    Determines next move for computer player
    
    Returns tuple of next move and boolean if it creates a winning condition.
    """
    WIN = True
    NO_WIN = False
    
    # check for winner
    for possible in range(0, 9):
        if board[possible] == EMPTY:        
            for winner in WINNERS:
                winner = list(winner)
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == mark and board[winner[1]] == mark:
                        return possible, WIN
            
    # check for block
    opp_mark = "O" if mark == "X" else "X"
    for possible in range(0, 9):
        if board[possible] == EMPTY:        
            for winner in WINNERS:
                winner = list(winner)
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == opp_mark and board[winner[1]] == opp_mark:
                        return possible, NO_WIN
    
    # if first move, place mark in corner
    if 'X' not in board and 'O' not in board:
        return choice(CORNERS), NO_WIN
    
    # check for empty center cell
    if board[CENTER] == EMPTY:
        return CENTER, NO_WIN
    
    # check for empty corner
    for possible in CORNERS:
        if board[possible] == EMPTY:
            return possible, NO_WIN
        
    # check for remaining empty cell
    for possible in EDGES:
        if board[possible] == EMPTY:
            return possible, NO_WIN
    
    # no possible move
    return -1, NO_WIN

