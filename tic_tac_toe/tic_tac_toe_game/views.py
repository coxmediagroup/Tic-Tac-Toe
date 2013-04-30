import json

from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from analytics.models import Event
from communications.communications import EmailCommunication

from .game_engine import GameEngine


def game(request):
    """
    Display blank game board, reset session variables, and record a game
    start event.

    """
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
    """
    Process Ajax requests received from client containing player moves.

    The method requires the HTTPRequest object to be an ajax request to
    function properly (it won't do anything otherwise).

    The method is a little long and could probably be broken up.  In lieu
    of that, it has numerous comments.

    """
    if request.is_ajax():

        # Get previous computer/player moves from session.
        player_moves = request.session['player_moves']
        computer_moves = request.session['computer_moves']

        # Does current move attempt to take already occupied space?
        for move_list in [player_moves, computer_moves]:
            if int(request.POST['id']) in move_list:
                json_response = {
                    'error_message': (
                        "You seem to lack a basic understanding "
                        "of the rules. You can't pick a previously "
                        "selected space.")
                }
                break

        else:
            # Add new move player to move history.
            player_moves.append(int(request.POST['id']))

            # Re-save player move list into session.
            request.session['player_moves'] = player_moves

            # Determine next computer move and add it to move history.
            game_engine = GameEngine(
                request.session['player_moves'],
                request.session['computer_moves'])

            next_computer_move, game_status = game_engine.next_computer_move()
            computer_moves.append(next_computer_move)

            # Re-save computer move list into session.
            request.session['computer_moves'] = computer_moves

            # What to do if the game is over and the computer won.
            if game_status == "Game Over (Computer Win)":
                email_message = EmailCommunication(
                    'grand-chiefain-of-the-moose-people@RGamesR2Smart4U.com',
                    [request.user.email],
                    '//OH SNAP!',
                    'email/lost_game.html',
                    {'first_name': request.user.first_name})

                email_message.send_message()

                analytics_event = Event(
                    event_type='TIC_TAC_TOE_FINISH_LOST',
                    event_url=request.path,
                    event_model=request.user.__class__.__name__,
                    event_model_id=request.user.id)

                analytics_event.save()

            # What to do if the game is over and ended in a draw.
            elif game_status == "Draw":
                email_message = EmailCommunication(
                    'grand-chiefain-of-the-moose-people@RGamesR2Smart4U.com',
                    [request.user.email],
                    '//YOU ALMOST WON!',
                    'email/draw_game.html',
                    {'first_name': request.user.first_name})

                email_message.send_message()

                analytics_event = Event(
                    event_type='TIC_TAC_TOE_FINISH_DRAW',
                    event_url=request.path,
                    event_model=request.user.__class__.__name__,
                    event_model_id=request.user.id)

                analytics_event.save()

            # Return most recent moves and game status to the client.
            json_response = {
                'player_move': player_moves[-1],
                'player_moves': player_moves,
                'computer_move': computer_moves[-1],
                'computer_moves': computer_moves,
                'game_status': game_status
            }

        return HttpResponse(
            json.dumps(json_response),
            mimetype="application/json")


def results(request):
    raise NotImplementedError