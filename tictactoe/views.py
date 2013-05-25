import json
import logging
from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin, ProcessFormView
from tictactoe import Board, NAUGHT, CROSS, EMPTY, naught_bot
from tictactoe.exceptions import TicTacToeError

LOG = logging.getLogger('tictactoe.views')


class BoardMixin(object):
    """manages the retrival and persistance of board data in the session"""

    def get_board(self):
        cells = self.request.session.get('cells', None)
        if cells is None:
            return Board()
            # The first player param is a formality at this point since the
        # human always goes first (right now).
        return Board(cells=cells, first_player=CROSS)

    def save_board(self, board):
        self.request.session['cells'] = list(board.cells)

    def reset_board(self):
        del self.request.session['cells']


class PlayGameView(BoardMixin, TemplateView):
    """Front page allows the user to start a new game and play to the end."""
    template_name = 'play-game.html'

    @staticmethod
    def __rows(board):
        """
        :return: generator of sets of 3 cells
        """
        cells = list(enumerate(board.cells))
        yield cells[0:3]
        yield cells[3:6]
        yield cells[6:9]

    def get_context_data(self, **kwargs):
        context = super(PlayGameView, self).get_context_data(**kwargs)
        board = self.get_board()
        context['cells'] = self.__rows(board)
        context['NAUGHT'] = NAUGHT
        context['CROSS'] = CROSS
        context['EMPTY'] = EMPTY
        context['board_is_empty'] = all(cell is EMPTY for cell in board.cells)
        context['game_is_over'] = board.game_is_over()
        context['winner'] = board.winner

        if self.get_board().game_is_over():
            self.reset_board()
        return context


class MarkForm(forms.Form):
    cell = forms.IntegerField(required=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(8)
    ])


class MakeMarkView(BoardMixin, FormMixin, ProcessFormView):
    """Update the active game board by placing the user's mark, then letting
    the bot make its own."""

    http_method_names = ('post', )
    form_class = MarkForm

    def form_invalid(self, form):
        raise ValueError

    def form_valid(self, form):
        board = self.get_board()
        LOG.debug(form.cleaned_data["cell"])

        # Normally I frown on initializing names prior to entering a
        # block where it *might* be defined so that it can safely be referenced
        # afterward, but meh.
        # Hi haters.
        exc = ""
        response = None

        try:
            board[form.cleaned_data["cell"]] = CROSS
            board[naught_bot(board)] = NAUGHT
            response = redirect(reverse('play-game'))
        except TicTacToeError as exc:
            LOG.exception(exc)
            LOG.exception(str(exc))
        finally:
            self.save_board(board)

            if self.request.is_ajax():
                response = HttpResponse(json.dumps({
                    'cells': list(board.cells),
                    'gameIsOver': board.game_is_over(),
                    'winner': board.winner,
                    'error': str(exc) or None,
                    }), content_type='application/json')

                # When working with ajax, we don't need a page reload to
                # display the win/draw board state so we reset right away.
                if board.game_is_over():
                    self.reset_board()

        return response
