import json
import random
import time

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse


def cell_list():
    """ assemble a list of cell lables for a tic-tac-toe board"""
    cell_list = []
    for row in ['top','middle','bottom']:
        for col in ['left','center','right']:
            cell_list.append(col + ' ' + row)
    return cell_list        


def json_response(status='OK', value=None):
    retval = {'status': status}
    if value is not None:
        retval['value'] = value

    response = HttpResponse(json.dumps(retval), mimetype='application/json')
    return response


def get_current_board(request):
    if 'board' not in request.session:
        request.session['board'] = ['',] * 9
    
    return request.session['board']


def board(request):
    # if a board does not yet exist, make one
    board_list = get_current_board(request)
    cells = cell_list()
    my_board = [zip(cells[:3], board_list[:3], range(0,3)),
                zip(cells[3:6], board_list[3:6], range(3,6)),
                zip(cells[6:], board_list[6:], range(6,9))]
    return render_to_response('board.html',
                              {'board': my_board},
                              context_instance=RequestContext(request))


def clear(request):
    if 'board' in request.session:
        del request.session['board']
    return json_response()


def user(request):
    cell_id = request.GET.get('cell_id', None)
    player = request.GET.get('player', None)
    if not cell_id or not player:
        return json_response('error')
    try:
        cell = int(cell_id)
    except ValueError:
        return json_response('error')

    board = get_current_board(request)
    if board[cell] != '':
        return json_response('error')

    board[cell] = player
    request.session['board'] = board
    return json_response()


def server(request):
    time.sleep(0.25)
    player = request.GET.get('player', None)
    if not player:
        return json_response('error')

    board = get_current_board(request)
    open_cells = []
    for idx, cell in enumerate(board):
        if cell == '':
            open_cells.append(idx)
            
    if not open_cells:
        return json_response('over')
    
    val = random.choice(open_cells)
    board[val] = player
    request.session['board'] = board

    return json_response(value=val)
