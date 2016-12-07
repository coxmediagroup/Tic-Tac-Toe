from django import forms

OPTION_CHOICES = (
    (True, 'YES'),
    (False, 'NO'),
)

class OptionsForm(forms.Form):
    computer_first = forms.ChoiceField(choices=OPTION_CHOICES, widget=forms.RadioSelect())
    