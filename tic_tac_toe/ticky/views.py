from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _

from tic_tac_toe import game

def _get_game(request):
    ttt = request.session.get('ttt', None)
    if not ttt:
        ttt = game.TicTacToe()
        request.session['ttt'] = ttt
    return ttt

def _get_status_message(ttt):
    status = ttt.get_status()
    if status == game.USER:
        status = _('Congratulations, you won!  How did you do that?')
    elif status == game.COMPUTER:
        status = _('You lose.  You are no match for the master!')
    elif status == game.DRAW:
        status = _("It's a draw!")
    else:
        status = 'Choose a position.'
    return status

def gameboard(request, template_name='ticky/game.html'):
    """
    Displays the playable gameboard.
    """
    ttt = _get_game(request)
    return render_to_response(template_name, RequestContext(request, {
        'game': ttt,
        'status': _get_status_message(ttt),
        'gameover': ttt.get_status() is not None,
    }))

def play(request):
    """
    Responds to user gameplay and redirects to `gameboard`.
    """
    # A valid post will contain exactly one input with key "x_y" or "replay".
    if not request.POST or len(request.POST) != 1:
        raise Http404, _('Invalid play specified.')

    command = request.POST.keys()[0]

    # Handle new game.
    if command == 'replay':
        request.session['ttt'] = None
        ttt = _get_game(request)

    # Handle play at (x, y).
    else:
        try:
            x, y = command.split('_')
            ttt = _get_game(request)
            ttt.play(int(x), int(y))
            request.session['ttt'] = ttt
        except ValueError:
            raise Http404, _('Invalid POST key %s.' % command)

    # If ajax request, return game status as json.
    if request.is_ajax():
        data = {
            'status': _get_status_message(ttt),
            'gameover': ttt.get_status() is not None,
            'positions': {
                '%s_%s' % (pos.x, pos.y): pos.value
                    for row in ttt.board for pos in row
            }
        }
        return HttpResponse(simplejson.dumps(data),
            mimetype='application/json')

    # If non-ajax POST, redirect to gameboard.
    else:
        return HttpResponseRedirect(reverse(gameboard))
