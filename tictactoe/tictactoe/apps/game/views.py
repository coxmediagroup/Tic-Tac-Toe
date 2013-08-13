import json
import random

from django.http import HttpResponse
from django.shortcuts import render


WINNING_COMBOS = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7),
)

NEIGHBORS = {
    1: (2, 4),
    2: (1, 3),
    3: (2, 6),
    4: (1, 7),
    6: (3, 9),
    7: (4, 8),
    8: (7, 9),
    9: (6, 8),
}

EMPTY_GAME = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
    8: '',
    9: '',
}


def JsonResponse(request, game, winning_combo=None):
    request.session['game'] = game
    rval = {
        'game': game,
        'winning_combo': winning_combo,
    }
    return HttpResponse(json.dumps(rval), mimetype='application/json')


def moves(game):
    counter = 0
    for move in game:
        if game[move] != '':
            counter += 1
    return counter


def index(request):
    game = request.session.get('game', EMPTY_GAME)
    return render(request, 'index.html', {
        'game_data': game,
    })


def next_move(request):
    clicked = request.GET.get('clicked')
    if not clicked:
        return HttpResponse('No cell click submitted')
    clicked = int(clicked)
    game = request.session.get('game', EMPTY_GAME)
    if game[clicked] != '':
        return HttpResponse('Cell already occupied')

    game[clicked] = 'x'

    if moves(game) == 1:
        # on the first move I'll take the middle
        if game[5] == '':
            game[5] = 'o'
        # unless the middle is taken, then I'll take a random corner
        else:
            game[random.choice((1, 3, 7, 9))] = 'o'
        return JsonResponse(request, game)
    else:
        # Look for a potential winning combo to block or win
        play = None
        winning = None
        for combo in WINNING_COMBOS:
            x_count = 0
            o_count = 0
            empty = 0
            for num in combo:
                if game[num] == 'x':
                    x_count += 1
                elif game[num] == 'o':
                    o_count += 1
                else:
                    empty = num
            blank_count = 3 - x_count - o_count
            if blank_count == 1:
                if o_count == 2:
                    winning = combo
                    play = empty
                    break
                if x_count == 2:
                    play = empty
        if play:
            game[play] = 'o'
            return JsonResponse(request, game, winning)

        # Or pick a neighboring cell
        neighbors = list(NEIGHBORS[clicked])
        random.shuffle(neighbors)
        for n in neighbors:
            if game[n] == '':
                game[n] = 'o'
                return JsonResponse(request, game)

        # Or pick any remaining spots available
        for i, cell_no in enumerate(game):
            if game[cell_no] == '':
                game[cell_no] = 'o'
        return JsonResponse(request, game)


def reset(request):
    request.session['game'] = EMPTY_GAME
    return HttpResponse('Game reset')
