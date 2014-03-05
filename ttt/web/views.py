from django.shortcuts import render
from django.http import HttpResponseRedirect

from tic_tac_toe import TicTacToe, DisplayTicTacToe

def get_params(request):
    """
    Get player paramters.
    """
    return render(request, 'start.html')

def play(request):
    if request.method == 'POST':
        # This is if the player wants to go first.
        # first param is if AI goes first
        if request.POST['go_first'] == 'Y':
            go_first = False
        else:
            go_first = True

        ttt = TicTacToe(xo=request.POST['mark'], first=go_first)

        request.session['ttt'] = ttt

    if 'ttt' not in request.session:
        return HttpResponseRedirect('/') 
    else:
        display = DisplayTicTacToe(request.session['ttt'])
        return render(request, 'play.html', {'display': display.as_dict()})


