from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signin_view(request):
    if request.method == 'POST':
        mail = request.POST["mail"]
        username = request.POST["username"]
        password = request.POST["password"]
        verify_password = request.POST["verify_password"]
    else:
        return render(request, 'users/signin_view.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', { 'error': 'Le pseudo ou le mot de passe est invalide' })
    else:
        return render(request, 'users/login.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
    else:
        return render(request, 'users/profile.html')


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/home.html')
