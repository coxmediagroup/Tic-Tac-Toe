from django import forms


class MoveForm(forms.Form):
    move = forms.IntegerField(required=True)
