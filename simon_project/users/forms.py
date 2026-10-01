from django import forms
from django.contrib.auth.models import User


class SigninForm(forms.ModelForm):
    verify_password = forms.CharField(label="Confirmation mot de passe", max_length=100)
    class Meta:
        model = User
        fields = ["email", "username", "password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]