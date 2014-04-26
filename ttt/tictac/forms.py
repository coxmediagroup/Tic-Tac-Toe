
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tictac.models import Board, Game
from tictac.constants import SYMBOL_CHOICES

class NewGameForm(forms.Form):
    player1 = forms.CharField(label=_('Player 1 Name'), max_length=64,
        widget=forms.TextInput(attrs={'placeholder': 'Player 1',
            'autofocus':'autofocus'}), required=False, )
    player1_auto = forms.ChoiceField(label=_('Player 1 is a '),
        choices=( (False, 'real person'), (True, 'the computer') ),
        widget=forms.RadioSelect, )
    player1_symbol = forms.CharField(label=_('Symbol '),
        required=False )
    player2 = forms.CharField(label=_('Player 2 Name'), max_length=64,
        required=False)
    player2_auto = forms.ChoiceField(label=_('Player 2 is a '),
        choices=( (False, 'real person'), (True, 'the computer') ),
        widget=forms.RadioSelect, )
    player2_symbol = forms.CharField(label=_('Symbol '), required=False)
    game_type = forms.ChoiceField(label=('Game type'),
        choices=( ('classic', 'classic tic-tac-toe'), ), required=False, )

    def clean_game_type(self):
        self.cleaned_data['game_type'] = 'classic'
        return self.cleaned_data['game_type']

    def clean_player1_symbol(self):
        data = self.cleaned_data['player1_symbol']
        if not data:
            self.cleaned_data['player1_symbol'] = '0'
        return self.cleaned_data['player1_symbol']

    def clean_player2_symbol(self):
        data = self.cleaned_data['player2_symbol']
        if not data:
            self.cleaned_data['player2_symbol'] = '1'
        return self.cleaned_data['player2_symbol']

    def clean_player1(self):
        data = self.cleaned_data['player1']
        if not data:
            self.cleaned_data['player1'] = 'Anonymous'
        return self.cleaned_data['player1']

    def clean_player2(self):
        data = self.cleaned_data['player2']
        if not data:
            self.cleaned_data['player2'] = 'Anonymous'
        return self.cleaned_data['player2']

    def clean_player1_auto(self):
        data = self.cleaned_data['player1_auto']
        self.cleaned_data['player1_auto'] = data == 'True'
        return self.cleaned_data['player1_auto']


    def clean_player2_auto(self):
        data = self.cleaned_data['player2_auto']
        self.cleaned_data['player2_auto'] = data == 'True'
        return self.cleaned_data['player2_auto']

class PlayForm(forms.Form):
    position = forms.IntegerField(label=_('Which position'))
    player = forms.IntegerField(label=_('Which player'))
