import json
import random
from django.http import Http404
from django.views.generic import TemplateView, View
from tictactoe.apps.game import game


class GameBoardView (TemplateView):
    """
    Displays the gameboard to the user.
    """
    template_name = 'apps/game/tic-tac-toe.html'

    def get_context_data(self, **kwargs):
        context = super(GameBoardView, self).get_context_data(**kwargs)

        # retrieve the game from the session data, or create a new one if needed
        self.request.session.flush()  # temporary so that I can test new games with a browser refresh to start
        session_data = self.request.session.get('tictactoe')
        tictactoe = game.TicTacToe(user_starts=random.randint(0, 1), session_data=session_data)
        self.request.session['tictactoe'] = tictactoe.__dict__

        context.update({
            'game': tictactoe
        })
        return context


class SubmitMoveView (View):
    """
    Handles the AJAX game submissions submitted by the user.
    """
    def post(self, request, *args, **kwargs):
        # only accept ajax requests
        if not request.is_ajax():
            raise Http404