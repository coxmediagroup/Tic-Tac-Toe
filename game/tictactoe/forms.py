from django import forms


class MoveForm(forms.Form):
    row = forms.CharField(required=True)
    col = forms.CharField(required=True)
