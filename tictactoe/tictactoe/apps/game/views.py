import json
import random
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView, View
from tictactoe.apps.game.game import TicTacToe, InvalidMoveError


def create_game(request):
    """
    Helper function: Instantiate a game with existing session data if it exists. If we're creating a new game,
    randomly determine whether to give the computer the first move.
    """
    current_game = request.session.get('tictactoe')
    tictactoe = TicTacToe(current_game=current_game)

    if not current_game:
        if random.randint(0, 1):
            tictactoe.computer_move()
        save_game(request, tictactoe)

    return tictactoe


def save_game(request, game_instance):
    """
    Helper function: Save the existing game to the session data so that it can be retrieved on subsequent requests
    """
    request.session['tictactoe'] = game_instance.__dict__


class GameBoardView (TemplateView):
    """
    Displays the current gameboard to the user.
    """
    template_name = 'apps/game/tic-tac-toe.html'

    def get_context_data(self, **kwargs):
        context = super(GameBoardView, self).get_context_data(**kwargs)

        self.request.session.flush()  # temporary so that I can test new games with a browser refresh to start
        tictactoe = create_game(self.request)
        context.update({
            'game': tictactoe
        })
        return context


class SubmitMoveView (View):
    """
    Handles the AJAX game moves submitted by the user.
    """
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        tictactoe = create_game(request)

        try:
            move = int(request.POST.get("move", None))
            tictactoe.player_move(move)
        except (ValueError, TypeError, IndexError, InvalidMoveError):
            response = {'success': False, 'message': 'We are unable to process your move. It appears to be invalid. Please try again.'}
        else:
            if not tictactoe.winner:
                tictactoe.computer_move()
            response = {'success': True, 'game': tictactoe.__dict__}
        finally:
            save_game(request, tictactoe)


        return HttpResponse(json.dumps(response), content_type='application/json')