from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from tic_tac_toe import game

def _get_game(request):
    ttt = request.session.get('ttt', None)
    if not ttt:
        ttt = game.TicTacToe()
        request.session['ttt'] = ttt
    return ttt

def gameboard(request, template_name='ticky/game.html'):
    """
    Displays the playable gameboard.
    """
    ttt = _get_game(request)
    status = ttt.get_status()
    if status == game.USER:
        status = _('Congratulations, you won!  How did you do that?')
    elif status == game.COMPUTER:
        status = _('You lose.  You are no match for the master!')
    elif status == game.DRAW:
        status = _("It's a draw!")
    return render_to_response(template_name, RequestContext(request, {
        'game': ttt,
        'status': status
    }))

def play(request):
    """
    Responds to user gameplay and redirects to `gameboard`.
    """
    # A valid post will contain exactly one input with key "x_y" or "replay".
    if request.POST and len(request.POST) == 1:
        key = request.POST.keys()[0]
        if key == 'replay':
            request.session['ttt'] = None
        else:
            try:
                x, y = key.split('_')
                ttt = _get_game(request)
                ttt.play(int(x), int(y))
                request.session['tic_tac_toe_game'] = ttt
            except ValueError:
                raise Http404, _('Invalid POST key %s.' % key)
        return HttpResponseRedirect(reverse(gameboard))
    else:
        raise Http404, _('Invalid play specified.')
