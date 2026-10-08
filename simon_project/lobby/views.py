from django.shortcuts import render

def index(request):
    return render(request, "base.html")

def test_websocket(request):
    return render(request, "lobby/test_websocket.html")