
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from web.models import Board, Game


class NewGameForm(forms.Form):
    player1 = forms.CharField(label=_('Player 1 Name'), max_length=64)
    player1_auto = forms.ChoiceField(label=_('Player 1 is a '),
        choices=( ('person', 'real person'), ('computer', 'the computer') ),
        widget=forms.radioSelect, )
    player2 = forms.CharField(label=_('Player 2 Name'), max_length=64)
    player2_auto = forms.ChoiceField(label=_('Player 2 is a '),
        choices=( ('person', 'real person'), ('computer', 'the computer') ),
        widget=forms.radioSelect, )
