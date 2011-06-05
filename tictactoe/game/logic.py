"""
Tic-Tac-Toe game logic

This is the game logic for Tic-Tac-Toe that allows a computer player
to always win or draw a game. In keeping with the spirit of the Zen of
Python, the logic is kept fairly simple instead of using complex techniques
such as minimax algorithms and decision trees.
"""
from random import choice

__author__ = "Nick Schwane"

CORNERS = [0, 2, 6, 8]  # indexes of corner cells
EDGES = [1, 3, 5, 7]  # indexes of remaining edge cells
CENTER = [4]  # index of center cell
WINNERS = [  # all possible winning combinations
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
EMPTY = ' '  # an empty cell contains a space


def _search_cells(board, lists):
    """
    Search for next available cell
    
    Iterates through a list of lists to find the next available spot
    for the computer to place its mark in.
    """
    for l in lists:
        for possible in l:
            if board[possible] == EMPTY:
                return possible
    return -1


def _search_winners(board, mark):
    for possible in range(9):
        if board[possible] == EMPTY:        
            for winner in WINNERS:
                winner = list(winner)
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == mark and board[winner[1]] == mark:
                        return possible
    return False


def _should_place_edge(board, mark, opp_mark):
    """
    If human goes first and this is computer's 2nd move and
    edge spaces are all empty, place mark on edge.
    """
    if board.count(opp_mark) == 2 and board.count(mark) == 1:
        for edge in EDGES:
            if board[edge] != EMPTY:
                return False
        return True
    else:
        return False


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
    for i in range(9):
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
    possible = _search_winners(board, mark)
    if possible:
        return possible, WIN
            
    # check for block
    opp_mark = "O" if mark == "X" else "X"
    possible = _search_winners(board, opp_mark)
    if possible:
        return possible, NO_WIN
    
    # if first move, place mark in corner
    if 'X' not in board and 'O' not in board:
        return choice(CORNERS), NO_WIN
    
    if _should_place_edge(board, mark, opp_mark):
        return choice(EDGES), NO_WIN
    
    # Search remaining cells in order of center, corners, and edges
    return _search_cells(board, [CENTER, CORNERS, EDGES]), NO_WIN

