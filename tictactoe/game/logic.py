"""
Tic-Tac-Toe game logic
"""

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


def check_for_win(board, mark):
    """
    Check to see if their is a winning condition for the specified mark
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
        board.append(request.GET.get(str(i), ' '))
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
        if board[possible] == ' ':        
            for winner in WINNERS:
                winner = winner[:]
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == mark and board[winner[1]] == mark:
                        return possible, WIN
            
    # check for block
    opp_mark = "O" if mark == "X" else "X"
    for possible in range(0, 9):
        if board[possible] == ' ':        
            for winner in WINNERS:
                winner = winner[:]
                if possible in winner:
                    winner.remove(possible)
                    if board[winner[0]] == opp_mark and board[winner[1]] == opp_mark:
                        return possible, NO_WIN
    
    # check for empty cell
    for possible in range(0, 9):
        if board[possible] == ' ':
            return possible, NO_WIN
    
    # no possible move
    return -1, NO_WIN

