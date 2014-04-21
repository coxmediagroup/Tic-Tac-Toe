import random


def take_center(board):
    move(board, **{'row': '1', 'col': '1'})


def take_corner(request):
    # There are 4 possible corners: [0][0], [0][2], [2][0], [2][2]
    # corners = ["0,0", "0,2", "2,0", "2,2"]
    mv = {
        'row': random.choice('0220'),
        'col': random.choice('0220')
    }
    move(request, **mv)


def move(request, letter='X', **kwargs):
    row = int(kwargs['row'])
    col = int(kwargs['col'])

    board = request.session['board']
    board[row][col] = letter
    request.session['board'] = board


def move_ai(request):
    board = request.session['board']
    """
    TODO Logic:
    Find the best move/position for AI
    If player didn't take the center, then AI takes the center

    Check if AI can win, if so, then take move
    Check if player can win. if so, then block that move

    Otherwise, find best move/position for AI
    """
    return 2, 2
