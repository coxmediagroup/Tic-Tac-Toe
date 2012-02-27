import logging

from django import forms
from django.conf import settings

class TicTacToeForm(forms.Form):
    """
    Represents the hidden form status of the current game.
    """
    gameID = forms.IntegerField(required=True, widget=forms.HiddenInput())

class BoardSizeForm(forms.Form):
    """
    Form that controls the size of the game board.
    """
    BOARD_SIZES = (
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        )
    boardSize = forms.ChoiceField(choices=BOARD_SIZES, required=True, label='Board Size: ', initial=3)
    CHARACTER_CHOICES = (
        ('X', 'Player 1 (X)'),
        ('O', 'Player 2 (O)'),
        )
    playerCharacter = forms.ChoiceField(choices=CHARACTER_CHOICES, required=True, label='Character Choice: ')