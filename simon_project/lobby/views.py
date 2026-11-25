from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from . import game_logic
from .models import Game, Player
import secrets, string 
from django.db.models import Max, Count, Prefetch


def index_lobby(request):
    return render(request, "lobby/index.html", {"max_players": 4, "user": request.user})

def index(request):
    return render(request, "home.html", {"user": request.user})

def test_websocket(request):
    return render(request, "lobby/test_websocket.html", {"user": request.user})

@login_required
def join_game(request):
    if request.method == "POST":
        code = request.POST.get("code", "").strip().upper()
        if Game.objects.filter(code=code).exists():
            return redirect("lobby:room", code=code)
        else:
            return render(request, "lobby/join_game.html", {"error": "This room does not exist.", "user": request.user})
    return render(request, "lobby/join_game.html", {"user": request.user})

def room(request, code):
    game = get_object_or_404(Game, code=code)
    is_in_game = request.user.is_authenticated and game.players.filter(user=request.user).exists()
    if game.launched and is_in_game:
        return redirect("lobby:play", code=code)
    players = list(game.players.order_by("order"))
    slots = players + [None] * (4 - len(players))
    return render(request, "lobby/room.html", {"game": game, "slots": slots, "is_in_game": is_in_game, "user": request.user})


@login_required
def play(request, code):
    game = get_object_or_404(Game, code=code)
    if not game.launched or not game.players.filter(user=request.user).exists():
        return redirect("lobby:room", code=code)
    return render(request, "lobby/game.html", {"game": game, "user": request.user})


@login_required
def leave(request, code):
    game = get_object_or_404(Game, code=code)
    if request.method == "POST":
        game_logic.leave_game(code, request.user)

        layer = get_channel_layer()
        etat = game_logic.get_state(code)
        players = [p["name"] for p in etat["players"]]
        async_to_sync(layer.group_send)("game_" + code, {
            "type": "players_update",
            "players": players,
        })
        async_to_sync(layer.group_send)("game_" + code, {
            "type": "state_update",
            "state": etat,
        })
    return redirect("lobby:index")

def get_public_games():
    """Public games that are not started, not full, not empty."""
    players = Player.objects.select_related("user").order_by("order")
    return (
        Game.objects.filter(is_public=True, launched=False)
        .annotate(nb=Count("players"))
        .filter(nb__gte=1, nb__lt=4)
        .prefetch_related(Prefetch("players", queryset=players))
        .order_by("-created_at")
    )


@login_required
def public_games(request):
    """Partial page refreshed by htmx on the join page."""
    return render(request, "lobby/_public_games.html", {"games": get_public_games()})


@login_required
def join_game(request):
    context = {"games": get_public_games(), "user": request.user}
    if request.method == "POST":
        code = request.POST.get("code", "").strip().upper()
        if Game.objects.filter(code=code).exists():
            return redirect("lobby:room", code=code)
        context["error"] = "This room does not exist."
    return render(request, "lobby/join_game.html", context)


@login_required
def create_game(request):
    if request.method == "POST":
        is_public = request.POST.get("is_public") == "on"
        code = generate_unique_code()
        game = Game.objects.create(code=code, is_public=is_public)
        Player.objects.create(user=request.user, game=game, order=0)
        return redirect("lobby:room", code=code)
    return render(request, "lobby/create_game.html", {"user": request.user})

def scores(request):
    return render(request, "lobby/scores.html", {"user": request.user})
       
def generate_unique_code():
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        if not Game.objects.filter(code=code).exists():
            return code
    