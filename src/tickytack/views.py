import json
import time

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

from tickytack.engines import MinMax

_marker = object()


def cell_list():
    """ assemble a list of cell lables for a tic-tac-toe board"""
    cell_list = []
    for row in ['top', 'middle', 'bottom']:
        for col in ['left', 'center', 'right']:
            cell_list.append(col + ' ' + row)
    return cell_list


def json_response(status='ok', value=None, player=None):
    retval = {'status': status}
    if value is not None:
        retval['value'] = value
    if player is not None:
        retval['player'] = player

    response = HttpResponse(json.dumps(retval), mimetype='application/json')
    return response


def new_board():
    board = ['', ] * 9
    return board


def get_current_board(request):
    if 'board' not in request.session:
        request.session['board'] = new_board()

    return request.session['board']


def clear(request):
    """ remove the existing board, if there is one, and set a new one
    """
    if 'board' in request.session:
        del request.session['board']
    request.session['board'] = new_board()
    return json_response()


def board(request):
    # always start with a new board
    board_list = new_board()
    cells = cell_list()
    my_board = [zip(cells[:3], board_list[:3], range(0, 3)),
                zip(cells[3:6], board_list[3:6], range(3, 6)),
                zip(cells[6:], board_list[6:], range(6, 9))]
    return render_to_response('board.html',
                              {'board': my_board},
                              context_instance=RequestContext(request))


def move(request):
    cell_id = request.GET.get('cell_id', _marker)
    player = request.GET.get('player', _marker)
    if player == _marker:
        # we don't know who's turn it is.  error out
        return json_response('error')

    board = get_current_board(request)

    cell = None
    if cell_id == _marker:
        # the computer did this one.  Make a move
        time.sleep(0.25)
        engine = MinMax(board, player)
        score, cell = engine.choose(8, -999999, 999999)
        board[cell] = player
    else:
        # the human did it, check the incoming value
        try:
            cell = int(cell_id)
        except ValueError:
            return json_response('error')
        else:
            # make a new engine with the player's choice and get the score
            board[cell] = player

    request.session['board'] = board
    engine = MinMax(board, player)
    score = engine.score

    if engine.is_terminal:
        if abs(score) > 200:
            return json_response('win', value=cell, player=player)
        else:
            return json_response('tie', value=cell, player=player)

    return json_response(value=cell, player=player)
