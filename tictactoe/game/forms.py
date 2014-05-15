from django import forms

class NewGameForm(forms.Form):
    player_first = forms.BooleanField(required=False, label="Would you like to go first?")

class MoveForm(forms.Form):
    x = forms.IntegerField()
    y = forms.IntegerField()

