from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from tic_tac_toe import TicTacToe, DisplayTicTacToe

def get_params(request):
    """
    Get player paramters.
    """
    return render(request, 'start.html')

def start(request):
    """
    Start the game off.
    """
    if request.method == 'POST':
        # This is if the player wants to go first.
        # first param is if AI goes first
        if request.POST['go_first'] == 'Y':
            go_first = False
        else:
            go_first = True

        if request.POST['mark'] == 'X':
            mark = 'O'
        else:
            mark = 'X'

        ttt = TicTacToe(xo=mark, first=go_first)
        request.session['ttt'] = ttt

    if 'ttt' not in request.session:
        return HttpResponseRedirect(reverse('get_params')) 
    else:
        return HttpResponseRedirect(reverse('play'))

def play(request):
    """
    Make player move and then ai move.
    """
    ttt = request.session['ttt']
    if request.method == 'POST':
        if 'ttt' not in request.session:
            return HttpResponseRedirect('/') 
        idx = request.POST['move']

        ttt.make_move(int(idx))
        ttt.ai_move()

        request.session['ttt'] = ttt

    won = ttt.won()
    display = DisplayTicTacToe(ttt)
    return render(request, 'play.html', {'display': display.as_dict(), 
                                         'won': won})

