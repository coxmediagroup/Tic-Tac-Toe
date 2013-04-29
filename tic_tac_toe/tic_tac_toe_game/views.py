import json

from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from analytics.models import Event


def game(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/usermanagement/login')

    template = loader.get_template('game.html')
    context = RequestContext(request)

    analytics_event = Event(
        event_type='TIC_TAC_TOE_START',
        event_url=request.path,
        event_model=request.user.__class__.__name__,
        event_model_id=request.user.id
    )
    analytics_event.save()

    # Retrieve past moves from session.
    request.session['player_moves'] = []
    request.session['computer_moves'] = []

    return HttpResponse(template.render(context))


def process_player_move(request):
    if request.is_ajax():

        # Get previous computer/player moves from session.
        player_moves = request.session['player_moves']
        computer_moves = request.session['computer_moves']

        json_response = {
            'player_move': int(request.POST['id']),
            'computer_move': int(request.POST['id']) + 2
        }

        return HttpResponse(
            json.dumps(json_response),
            mimetype="application/json")


def results(request):
    pass