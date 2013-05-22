import logging
from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin, ProcessFormView
from tictactoe import Board, NAUGHT, CROSS, EMPTY, naught_bot
from tictactoe.exceptions import GameOver

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
    """Front page allows the user to start a new game."""
    template_name = 'play-game.html'

    def get_context_data(self, **kwargs):
        context = super(PlayGameView, self).get_context_data(**kwargs)
        context['cells'] = enumerate(self.get_board().cells)
        context['NAUGHT'] = NAUGHT
        context['CROSS'] = CROSS
        context['EMPTY'] = EMPTY
        return context

    def get(self, request, *args, **kwargs):
        if self.get_board().game_is_over():
            return redirect(reverse('game-over'))
        else:
            return super(PlayGameView, self).get(request, *args, **kwargs)


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
        try:
            board[form.cleaned_data["cell"]] = CROSS
            board[naught_bot(board)] = NAUGHT
        except GameOver as exc:
            LOG.exception(exc)
            LOG.exception(exc.message)
            return redirect(reverse('game-over'))
        finally:
            self.save_board(board)

        return redirect(reverse('play-game'))


class GameOverView(BoardMixin, TemplateView):
    template_name = 'game-over.html'

    def get_context_data(self, **kwargs):
        context = super(GameOverView, self).get_context_data(**kwargs)
        context['winner'] = self.get_board().winner
        context['NAUGHT'] = NAUGHT
        context['CROSS'] = CROSS
        return context

    def get(self, request, *args, **kwargs):
        resp = super(GameOverView, self).get(request, *args, **kwargs)
        try:
            self.reset_board()
        except KeyError:
            return redirect(reverse('play-game'))
        return resp