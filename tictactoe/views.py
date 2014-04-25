import json

from django.shortcuts import render
import django.core.urlresolvers
import django.http.response


def json_response(data):
    """Create an HttpResponse with data converted to JSON."""
    response_body = json.dumps(data)
    return django.http.response.HttpResponse(response_body,
                                             content_type="application/json")


def handle_move(request):
    """Process the player's move and make a move in response."""

    # stubbed for now
    game_board = [
        '  o',
        '   ',
        '   ',
    ]

    return json_response({'board': game_board})



def show_game(request):
    """A hello-world test view."""

    game_board = [
        '   ',
        '   ',
        '   ',
    ]

    ai_service = django.core.urlresolvers.reverse(handle_move)

    context = {
        'board': game_board,
        'ai_url': ai_service,
    }

    return render(request, "tictactoe/game.html.djt", context)