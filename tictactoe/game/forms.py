import logging

from django import forms
from django.conf import settings

class TicTacToeForm(forms.Form):
    """
    Represents the hidden form status of the current game.
    """
    gameID = forms.IntegerField(required=True, widget=forms.HiddenInput())
