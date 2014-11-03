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

    X always moves first.
    If board.count('-') % 2 == 1, then it's X's turn.

    "Best Move" is the available move on turn n1 that satisfies the highest
    priority:

    1.)  Win the game.
    2.)  Don't lose the game. No moves on board board_n2 result in a win.
    3.)  Win the game on turn n3.  Is a non-loss above and 2 or more available
         moves on board_n3 are wins.
    4.)  Don't lose the game on board_n4. Is a non-loss above and no more than
         one 
    5.)  On an empty board, grab a corner.
    6.)  On a non-empty board, grab the center, if possible.
    7.)  On a non-empty board with the center taken, grab a corner.
"""

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


# Text Friendly Board Representation
def pretty_board(board):
    return board[0:3] + '\n' + board[3:6] + '\n' + board[6:9]


# Check board for a Win
# If player is provided, check it for a win for only that player
def is_win(board, player = None):
    current_lines = [ ''.join([ board[p] for p in line ]) for line in lines ]
    if player is not None:
        return (3*player in current_lines)
    return ('xxx' in current_lines) or ('ooo' in current_lines)


# Get the indicies of legal moves
def get_legal_moves(board):
    return [ i for i, c in enumerate(board) if c == '-' ]


# Make a move and return the resulting board
def apply_move(point, board, player):
    board_list = list(board)
    board_list[point] = player
    return ''.join(board_list) 


example_board = 'x--oo-x--'


# Given a board, get the next best move
# returns a tuple in the format (move, board, player)
def get_best_move(board, depth=-1):
    #keep up with the relative depth
    depth = depth + 1

    player = 'x' if board.count('-') % 2 == 1 else 'o' 

    # list of possible moves
    moves = get_legal_moves(board)

    # if the board is empty, take 0
    if board.count('-') == 9:
        return 0, apply_move(0, board, player), player

    # if the board has only one piece placed, take center
    if board.count('-') == 8 and board[4] == '-':
        return 4, apply_move(4, board, player), player

    # if the board has only one piece placed and center is taken, take 0
    if board.count('-') == 8 and board[4] == 'x':
        return 0, apply_move(4, board, player), player

    # if the board has only one possible move, take it
    if len(moves) == 1:
        return moves[0], apply_move(moves[0], board, player), player

    # dict of outcomes of possible moves
    # move : (board, win?)
    results = { m : (
        apply_move(m, board, player),
        is_win(apply_move(m, board, player), player)
        ) for m in moves }
    
    # if one of the moves results in a win, take it
    if [ k for k, v in results.iteritems() if v[1] is True ]:
        winning_move = [ k for k, v in results.iteritems() if v[1] == True ][0]
        return winning_move, apply_move(winning_move, board, player), player

    # if any of these moves results in a possible loss on oponent's next move,
    # prune them
    losing_moves = []
    for m in moves:
        print depth, m
        m2, b2, p2 = get_best_move(apply_move(m, board, player), depth)
        if is_win(b2, p2):
            losing_moves.append(m)
    
    for lm in losing_moves:
        moves.remove(lm)

    if len(moves) == 1:
        return moves[0], apply_move(moves[0], board, player), player

    # if one of these moves results in multiple possible wins on our next
    # turn, take them

    
    
    

    # if one of these moves results in multiple possible losses on opponents
    # next, next turn, prune them

    return -1, board, player 

