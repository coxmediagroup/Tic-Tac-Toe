from django import forms



class UsernameForm(forms.Form):
    username = forms.CharField(max_length=32)
