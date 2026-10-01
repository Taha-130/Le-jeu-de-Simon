from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    return render(request, "lobby/index.html", {"max_joueurs": 4})

def test(request):
    return HttpResponse("Hello, world. You're at the test lobby Taha.")