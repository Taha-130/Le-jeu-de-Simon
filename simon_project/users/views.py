from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.forms import SigninForm, LoginForm, ProfileForm


def signin_view(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            return redirect('users:profile')
    else:
        form = SigninForm()
        return render(request, 'users/signin.html', { 'form': form } )


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleanded_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
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
