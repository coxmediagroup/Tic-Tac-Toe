from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

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

    upper_row = None

    if request.method == "POST":

        if request.POST.get('reset'):
            return HttpResponseRedirect('http://127.0.0.1:8000/tic_tac_toe')

        a1 = request.POST.get('A1', '')
        a2 = request.POST.get('A2', '')
        a3 = request.POST.get('A3', '')
        b1 = request.POST.get('B1', '')
        b2 = request.POST.get('B2', '')
        b3 = request.POST.get('B3', '')
        c1 = request.POST.get('C1', '')
        c2 = request.POST.get('C2', '')
        c3 = request.POST.get('C3', '')
    
        cells = {
            'A1': a1, 'A2': a2, 'A3': a3,
            'B1': b1, 'B2': b2, 'B3': b3,
            'C1': c1, 'C2': c2, 'C3': c3 
        }
        winner = check_for_winner(cells)
        next_move = find_next_move(cells)

        cells[next_move] = 'X'

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
        'bottom_row': bottom_row,
        'winner': winner,
    }, RequestContext(request));

def check_for_winner(cells):

    if cells['A1']:
        if ( cells['A1'] == cells['A2'] ) and ( cells['A1'] == cells['A3'] ):
            return True
        elif ( cells['A1'] == cells['B1'] ) and ( cells['A1'] == cells['C1'] ):
            return True
        elif ( cells['A1'] == cells['B2'] ) and ( cells['A1'] == cells['C3'] ):
            return True
    if cells['B1']:
        if ( cells['B1'] == cells['B2'] ) and ( cells['B1'] == cells['B3'] ):
            return True
    if cells['C1']:
        if ( cells['C1'] == cells['C2'] ) and ( cells['C1'] == cells['C3'] ):
            return True
    if cells['A2']:
        if ( cells['A2'] == cells['B2'] ) and ( cells['A2'] == cells['C2'] ):
            return True
    if cells['A3']:
        if ( cells['A3'] == cells['B3'] ) and ( cells['A3'] == cells['C3'] ):
            return True
        elif ( cells['A3'] == cells['B2'] ) and ( cells['A3'] == cells['C1'] ):
            return True

    return False

def find_next_move(cells):

    # Check for win
    next_move = potential_win(cells, 'row', 'A', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'row', 'B', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'row', 'C', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'col', '1', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'col', '2', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'col', '3', 'X')
    if next_move:
        return next_move

    next_move = potential_win(cells, 'diagonal', '', 'X')
    if next_move:
        return next_move

    # Look for block in first row
    next_move = potential_win(cells, 'row', 'A', 'O')
    if next_move:
        return next_move

    # Look for block in second row
    next_move = potential_win(cells, 'row', 'B', 'O')
    if next_move:
        return next_move

    # Look for block in third row
    next_move = potential_win(cells, 'row', 'C', 'O')
    if next_move:
        return next_move

    # Look for block in first column
    next_move = potential_win(cells, 'col', '1', 'O')
    if next_move:
        return next_move

    # Look for block in second column
    next_move = potential_win(cells, 'col', '2', 'O')
    if next_move:
        return next_move

    # Look for block in third column
    next_move = potential_win(cells, 'col', '3', 'O')
    if next_move:
        return next_move

    # Look for diagonal block
    next_move = potential_win(cells, 'diagonal', '', 'O')
    if next_move:
        return next_move

    return None

def potential_win(cells, orientation, id, value):
    
    if ( orientation == 'row' ):
        if ( cells[id + '1'] == value and cells[id + '2'] == value and cells[id + '3'] == '' ):
            return id + '3'
        elif ( cells[id + '1'] == '' and cells[id + '2'] == value and cells[id + '3'] == value ):
            return id + '1'
        elif ( cells[id + '1'] == value and cells[id + '2'] == '' and cells[id + '3'] == value ):
            return id + '2'

    if ( orientation == 'col' ):
        if ( cells['A' + str(id)] == value and cells['B' + str(id)] == value and cells['C' + str(id)] =='' ):
            return 'C' + str(id)
        if ( cells['A' + str(id)] == '' and cells['B' + str(id)] == value and cells['C' + str(id)] == value ):
            return 'A' + str(id)
        if ( cells['A' + str(id)] == value and cells['B' + str(id)] == '' and cells['C' + str(id)] == value ):
            return 'B' + str(id)

    if ( orientation == 'diagonal' ):
        if ( cells['A1'] == value and cells['B2'] == value and cells['C3'] == '' ):
            return 'C3'
        elif ( cells['A1'] == value and cells['B2'] == '' and cells['C3'] == value ):
            return 'B2'
        elif ( cells['A1'] == '' and cells['B2'] == value and cells['C3'] == value ):
            return 'A1'
        if ( cells['A3'] == value and cells['B2'] == value and cells['C1'] == '' ):
            return 'C1'
        elif ( cells['A3'] == value and cells['B2'] == '' and cells['C1'] == value ):
            return 'B2'
        elif ( cells['A3'] == '' and cells['B2'] == value and cells['C1'] == value ):
            return 'A3'
