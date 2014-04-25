
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tictac.models import Board, Game
from tictac.constants import SYMBOL_CHOICES

class NewGameForm(forms.Form):
    player1 = forms.CharField(label=_('Player 1 Name'), max_length=64)
    player1_auto = forms.ChoiceField(label=_('Player 1 is a '),
        choices=( ('person', 'real person'), ('computer', 'the computer') ),
        widget=forms.RadioSelect, )
    player1_symbol = forms.ChoiceField(label=_('Symbol '),
        choices=(SYMBOL_CHOICES, ), required=False )
    player2 = forms.CharField(label=_('Player 2 Name'), max_length=64)
    player2_auto = forms.ChoiceField(label=_('Player 2 is a '),
        choices=( ('person', 'real person'), ('computer', 'the computer') ),
        widget=forms.RadioSelect, )
    player2_symbol = forms.ChoiceField(label=_('Symbol '),
        choices=(SYMBOL_CHOICES, ), required=False)
    game_type = forms.ChoiceField(label=('Game type'),
        choices=( ('classic', 'classic tic-tac-toe'), ), )


class PlayForm(forms.Form):
    position = forms.IntegerField(label=_('Which position'))
    player = forms.IntegerField(label=_('Which player'))
