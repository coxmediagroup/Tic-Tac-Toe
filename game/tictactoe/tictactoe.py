import random


def take_corner(request):
    """
    There are 4 possible corners = [0, 2, 6, 8]
    [
        '0', '1', '2',
        '3', '4', '5',
        '6', '7', '8'
    ]
    """
    corners = [0, 2, 6, 8]
    # TODO: Make sure it is not taken
    move(request, random.choice(corners))


def move(request, position, letter='X'):
    board = request.session['board']
    board[position] = letter
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
    return 2
