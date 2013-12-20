from django import forms

from . import models


class CreateGameForm(forms.ModelForm):
    class Meta:
        model = models.Game
        exclude = ('user', 'timestamp')


class MoveForm(forms.Form):
    row = forms.IntegerField(min_value=0, max_value=2)
    column = forms.IntegerField(min_value=0, max_value=2)

    def __init__(self, game, *args, **kwargs):
        self.game = game
        super(MoveForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(MoveForm, self).clean()

        row = cleaned_data.get('row')
        column = cleaned_data.get('column')

        position = self.game.positions.latest()
        if ' ' not in position.state or position.is_won():
            raise forms.ValidationError("This game is concluded.")

        if not position.is_legal((row, column)):
            raise forms.ValidationError(
                "The position ({0}, {1}) is already taken.".format(row, column)
            )

        return cleaned_data
