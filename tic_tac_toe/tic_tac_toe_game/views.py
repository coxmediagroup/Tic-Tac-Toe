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

        # Does current move attempt to take already occupied space?
        for move_list in [player_moves, computer_moves]:
            if int(request.POST['id']) in move_list:
                json_response = {
                    'error_message': 'That space is already taken.'
                }
                break

        else:
            player_moves.append(int(request.POST['id']))
            computer_moves.append(int(request.POST['id']) + 2)

            request.session['player_moves'] = player_moves
            request.session['computer_moves'] = computer_moves

            json_response = {
                'player_move': player_moves[-1],
                'computer_move': computer_moves[-1]
            }



        return HttpResponse(
            json.dumps(json_response),
            mimetype="application/json")


def results(request):
    pass