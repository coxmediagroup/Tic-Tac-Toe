from django.shortcuts import render_to_response
from django.template import RequestContext

from random import randrange

def index(request):

    # Computer plays first
    first_plays = [ 'B3', 'A2', 'B1', 'C2' ]

    first_play = randrange(0, 4)

    cells = {
        'A1': '', 'A2': '', 'A3': '',
        'B1': '', 'B2': '', 'B3': '',
        'C1': '', 'C2': '', 'C3': ''
    }

    cells[first_plays[first_play]] = 'X'

    upper_row = [ { 'index': 'A1', 'value': cells['A1'], 'position': 'left' }, 
        { 'index': 'A2', 'value': cells['A2'], 'position': 'center' }, 
        { 'index': 'A3', 'value': cells['A3'], 'position': 'right' } ]
    middle_row = [ { 'index': 'B1', 'value': cells['B1'], 'position': 'left' }, 
        { 'index': 'B2', 'value': cells['B2'], 'position': 'center' }, 
        { 'index': 'B3', 'value': cells['B3'], 'position': 'right' } ]
    bottom_row = [ { 'index': 'C1', 'value': cells['C1'], 'position': 'left' }, 
        { 'index': 'C2', 'value': cells['C2'], 'position': 'center' }, 
        { 'index': 'C3', 'value': cells['C3'], 'position': 'right' } ]

    return render_to_response('tic_tac_toe/tic_tac_toe.html', {
        'upper_row': upper_row,
        'middle_row': middle_row,
        'bottom_row': bottom_row
    }, RequestContext(request));

def user_move(request):
    return render_to_response('tic_tac_toe/tic_tac_toe.html', {
        'upper_row': None,
        'middle_row': None,
        'bottom_row': None
    }, RequestContext(request));
