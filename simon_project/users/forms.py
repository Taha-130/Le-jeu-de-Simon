from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    verify_password = forms.CharField(label="Password confirmation", max_length=100, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]