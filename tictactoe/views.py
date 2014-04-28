import json

from django.shortcuts import render
import django.core.urlresolvers
import django.http.response

import tictactoe_logic


def __json_response(data):
    """Create an HttpResponse with data converted to JSON."""
    response_body = json.dumps(data)
    return django.http.response.HttpResponse(response_body,
                                             content_type="application/json")


def __update_board(board, new_move):
    """Add the AI's move to the board.

    Returns None; changes board in-place.

    """
    ai_row, ai_col = new_move
    row = list(board[ai_row])  # strings are immutable, so convert to a list
    row[ai_col] = 'O'
    board[ai_row] = ''.join(row)  # convert back to a string and update board


def handle_move(request):
    """Process the player's move and make a move in response.

    This is an AJAX service. The request should be a POST with a JSON body,
    and it responds with JSON.

    The body is the game board model, as described in the ``tictactoe_logic``
    package docstring.

    """
    board = json.loads(request.body.decode())

    info = tictactoe_logic.check_board(board)
    if info.state == tictactoe_logic.INCOMPLETE:
        ai_piece, ai_move = tictactoe_logic.get_ai_move(board)
        __update_board(board, ai_move)
    info = tictactoe_logic.check_board(board)

    resp_data = {
        'board': board,
        'state': info.state.upper(),
    }

    return __json_response(resp_data)


def show_game(request):
    """Show an empty game board so a user can start playing."""

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