"""
This module performs 2 functions:
    1. determines if a tic-tac-toe game is over, and if so, provides additional
        details (was there a winner, and if so which player won, what was
        the location of the three-in-a-row, etc.)
    2. using the minmax algorithm, determines what the next move should be.

board is a list of 9 elements, representing 3 rows of 3 columns:
    0   1   2
    3   4   5
    6   7   8

"""

WINNING_POSITIONS_LIST = [
    (0,1,2), (3,4,5), (6,7,8),  # 3 across
    (0,3,6), (1,4,7), (2,5,8),  # 3 down
        (0,4,8), (2,4,6)        # 3 diagonal
]

def findBestScoreMove(board, playerChar='O'):
    """
    Evaluate all game positions and return best position for next move
    and its score as a tuple: (score, position)

    This utilizes the recursive minmax algorithm from game theory
    (http://en.wikipedia.org/wiki/Minimax#Combinatorial_game_theory)

    let m be the list of all available moves.

    score_move = []
    for pos in m:
        make move (change copy of board)
        if game would be over:
            calculate score for this move as:
                1 if playerChar wins
                0 if a draw
                -1 otherwise (opponent wins)
        else:
            calculate score for this move as:
                if playerChar is 'O':
                    opponentChar = 'X'
                else:
                    opponentChar = 'O'
                -1 * findBestScoreMove(board, opponentChar)[0]
        score_move.append((score, pos))

    # now find move/pos with highest score
    score_move.sort()
    return score_move[-1]
    """

    score_move = []
    for pos, val in enumerate(board):
        if val != '-': continue
        newBoard = list(board)      # make copy of board
        newBoard[pos] = playerChar
        status = gameIsOver(newBoard)
        if status:  # game would be over
            winner = status[0]
            if winner == playerChar:    # player playerChar wins
                score = 1
            elif winner == '':      # draw
                score = 0
            else:                   # opponent wins
                score = -1
        else:
            if playerChar == 'O':
                opponentChar = 'X'
            else:
                opponentChar = 'O'
            score = -1 * (findBestScoreMove(newBoard, opponentChar)[0])
        score_move.append((score, pos))

    # now find move/pos with highest score
    score_move.sort()
    return score_move[-1]


def gameIsOver(board):
    """
    if three-in-a-row exists:   # someone won
        return (winner, positions) where:
            winner = 'O|X'
            positions = three-tuple
    else if board is full:      # draw
        return ('', [])
    else:                       # game not over
        return False
    """

    # see if we have a winner
    for positions in WINNING_POSITIONS_LIST:
        a, b, c = positions
        char = board[a]
        if char != '-' and char == board[b] == board[c]:    # winner!
            return char, positions

    # see if it's a draw
    if '-' not in board:
        return '', []

    # game not over
    return False
