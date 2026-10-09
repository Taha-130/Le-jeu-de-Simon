from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Player
import secrets, string 


def index(request):
    return render(request, "lobby/index.html", {"max_joueurs": 4})

def test_websocket(request):
    return render(request, "lobby/test_websocket.html")

def room(request, code):
    game = get_object_or_404(Game, code=code)
    players = list(game.players.order_by("order"))
    slots = players + [None] * (4 - len(players))
    is_in_game = request.user.is_authenticated and game.players.filter(user=request.user).exists()
    return render(request, "lobby/room.html", {"game": game, "slots": slots, "is_in_game": is_in_game})


@login_required
def join(request, code):
    game = get_object_or_404(Game, code=code)
    if game.launched:
        return HttpResponse("La partie a déjà commencé.")
    if game.players.count() >= 4:
        return HttpResponse("Le salon est plein.")
    if game.players.filter(user=request.user).exists():
        return HttpResponse("Vous êtes déjà dans ce salon.")

    order = game.players.count()
    Player.objects.create(user=request.user, game=game, order=order)
    return redirect("room", code=code)

@login_required
def create_game(request):
    if request.method == "POST":
        code = generate_unique_code()
        game = Game.objects.create(code=code)
        Player.objects.create(user=request.user, game=game, order=0)
        return redirect("room", code=code)
    return redirect("index")
    
    
def generate_unique_code():
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        if not Game.objects.filter(code=code).exists():
            return code
            
    