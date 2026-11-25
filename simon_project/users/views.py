from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.forms import SignupForm, LoginForm, ProfileForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('lobby:index')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', { 'form': form } )


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('lobby:index')
            else:
                return render(request, 'users/login.html', { 'error': 'Le pseudo ou le mot de passe est invalide' })
    else:
        form = LoginForm()
    return render(request, 'users/login.html', { 'form': form } )


@login_required
def profile_view(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'users/profile.html', { 'user': request.user } )


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


# to explain to the user that they need to be logged in to access a page
def login_required_view(request):
    return render(request, 'users/login_required.html')
