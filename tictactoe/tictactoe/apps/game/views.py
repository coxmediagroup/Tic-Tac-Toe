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

        # create a new game with existing session data if it exists
        self.request.session.flush()  # temporary so that I can test new games with a browser refresh to start

        session_data = self.request.session.get('tictactoe')
        tictactoe = game.TicTacToe(session_data=session_data)

        # if session data was none, randomly decide if the computer should move first
        if not session_data and random.randint(0, 1):
            tictactoe.computer_move()

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


