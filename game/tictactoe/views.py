from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from game.http import JsonResponse

from .forms import MoveForm
from .tictactoe import (take_corner, move, move_ai, winner, AI_LETTER,
                        HUMAN_LETTER, is_tie)


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

    context = {
        'corner': corner,
        'moves': range(9),
        'active': start
    }
    return render(request, 'tictactoe/board.html', context)


@csrf_protect
def make_move(request):
    data = {
        'success': False
    }

    form = MoveForm(request.POST or None)
    if form.is_valid():
        move(request, form.cleaned_data['move'], HUMAN_LETTER)
        board = request.session['board']
        # Check if human move can tie/win
        if winner(board):
            # This should never happen
            data['win_status'] = 'human'
        elif is_tie(request):
            data['win_status'] = 'tie'
        else:
            # Computer move and check if it can win
            mv, is_winner = move_ai(board)
            board[mv] = AI_LETTER
            request.session['board'] = board
            data['move'] = mv

            if is_winner:
                data['win_status'] = 'computer'
                data['board'] = board
            elif is_tie(request):
                data['win_status'] = 'tie'
        data['success'] = True

    return JsonResponse(data)
