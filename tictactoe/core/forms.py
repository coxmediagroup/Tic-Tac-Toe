from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(render_value=False))
    
    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            return self.cleaned_data["username"]
        raise forms.ValidationError("This username is already taken. Please choose another.")
    
    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError("You must type the same password each time.")
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data["username"]
        email = ""
        password = self.cleaned_data["password1"]
        
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
                
        return username, password # required for authenticate()
