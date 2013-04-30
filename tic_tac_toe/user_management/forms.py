from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class UserForm(ModelForm):
    """
    This class is being used instead of the Django provided default in order
    to collect first_name, last_name, and email attributes.

    """

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        widgets = {
            'password': forms.PasswordInput
        }