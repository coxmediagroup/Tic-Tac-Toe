from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from game.http import JsonResponse

from .forms import MoveForm
from .tictactoe import take_corner, move, move_ai


def play(request):
    board = ['' for m in range(9)]
    """
    >>> board = ['' for m in range(9)]
    >>> board
    ['', '', '', '', '', '', '', '', '']
    """
    request.session['board'] = board
    start = request.GET.get('start', 'computer')
    if start != 'player':
        """
        According to: http://en.wikipedia.org/wiki/Tic-tac-toe

        Player X can win or force a draw from any of these starting marks;
        however, playing the corner gives the opponent the smallest choice of
        squares which must be played to avoid losing.
        """
        take_corner(request)

    return render(request, 'tictactoe/board.html', {})


@csrf_exempt
def make_move(request):
    data = {
        'success': False
    }

    form = MoveForm(request.POST or None)
    if form.is_valid():
        move(request, form.cleaned_data['move'])
        # TODO:
        # check if player can win
        # if not, then move_ai

        data['success'] = True
        data['move'] = move_ai(request)

        # TODO: check if ai can win

    return JsonResponse(data)
