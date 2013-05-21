from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin, ProcessFormView
from tictactoe import Board, NAUGHT, CROSS, EMPTY


class Game(TemplateView):
    """Front page allows the user to start a new game."""
    template_name = 'game.html'

    def get_board(self):
        return Board()


    def get_context_data(self, **kwargs):
        context = super(Game, self).get_context_data(**kwargs)
        context['cells'] = enumerate(self.get_board().cells)
        context['NAUGHT'] = NAUGHT
        context['CROSS'] = CROSS
        context['EMPTY'] = EMPTY
        return context


class MarkForm(forms.Form):
    cell = forms.IntegerField(required=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(8)
    ])


class MakeMark(FormMixin, ProcessFormView):
    """Update the active game board by placing the user's mark, then letting
    the bot make its own."""

    http_method_names = ('post', )
    form_class = MarkForm

    def form_invalid(self, form):
        pass

    def form_valid(self, form):
        pass