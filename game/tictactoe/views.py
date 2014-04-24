from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from game.http import JsonResponse

from .forms import MoveForm
from .tictactoe import (take_corner, move, move_ai, winner, AI_LETTER,
                        HUMAN_LETTER)


def play(request):
    board = ['' for m in range(9)]
    """
    >>> board = ['' for m in range(9)]
    >>> board
    ['', '', '', '', '', '', '', '', '']
    """
    corner = -1
    request.session['board'] = board
    start = request.GET.get('start', 'computer')
    if start != 'human':
        """
        According to: http://en.wikipedia.org/wiki/Tic-tac-toe

        Player X can win or force a draw from any of these starting marks;
        however, playing the corner gives the opponent the smallest choice of
        squares which must be played to avoid losing.
        """
        corner = take_corner(request)

    context = {'corner': corner}
    return render(request, 'tictactoe/board.html', context)


@csrf_exempt
def make_move(request):
    data = {
        'success': False
    }

    form = MoveForm(request.POST or None)
    if form.is_valid():
        move(request, form.cleaned_data['move'], HUMAN_LETTER)
        board = request.session['board']

        # Check if human move can win
        winner_move = winner(board)
        # TODO: If human starts, check here if it is a tie
        if winner_move:
            data['winner'] = 'human'
        else:
            # Check if AI can win
            mv, is_winner = move_ai(board)
            if is_winner:
                data['winner'] = 'ai'

            board[mv] = AI_LETTER
            request.session['board'] = board
            data['move'] = mv
        data['success'] = True

    return JsonResponse(data)
