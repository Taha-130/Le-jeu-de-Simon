from django.db import transaction
from django.utils import timezone
from .models import Game

COULEURS = ["rouge", "bleu", "vert", "jaune"]


def joueur_suivant(players, actuel):
    n = len(players)
    for i in range(1, n + 1):
        index = (actuel + i) % n
        if not players[index].eliminated:
            return index
    return actuel


def eliminer(game, players, index):
    players[index].eliminated = True
    players[index].save()

    vivants = [p for p in players if not p.eliminated]
    if len(vivants) > 1 and game.curr_player == index:
        game.curr_player = joueur_suivant(players, index)
        game.curr_step = 0
        game.turn_id += 1
        game.step_start_time = timezone.now()


def get_state(code):
    game = Game.objects.filter(code=code).first()
    if game is None:
        return None
    players = list(game.players.order_by("order"))
    vivants = [p for p in players if not p.eliminated]

    gagnant = None
    if game.launched and len(players) > 1 and len(vivants) == 1:
        gagnant = vivants[0].user.username

    courant = None
    if game.launched and players:
        courant = players[game.curr_player].user.username

    return {
        "launched": game.launched,
        "current": courant,
        "winner": gagnant,
        "length": len(game.sequence),
        "players": [
            {"name": p.user.username, "eliminated": p.eliminated} for p in players
        ],
    }


def start_game(code, user):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))

        if game.launched:
            return "La partie a déjà commencé.", None
        if not players or players[0].user != user:
            return "Seul le créateur peut lancer la partie.", None
        if len(players) < 2:
            return "Il faut au moins 2 joueurs.", None

        game.launched = True
        game.sequence = []
        game.curr_player = 0
        game.curr_step = 0
        game.turn_id += 1
        game.step_start_time = timezone.now()
        game.save()

        return None, players[0].user.username


def play_color(code, user, color):
    if color not in COULEURS:
        return "Couleur invalide.", None

    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))
        vivants = [p for p in players if not p.eliminated]

        if not game.launched:
            return "La partie n'a pas commencé.", None
        if len(vivants) <= 1:
            return "La partie est terminée.", None
        if players[game.curr_player].user != user:
            return "Ce n'est pas ton tour.", None

        erreur_couleur = False

        if game.curr_step == len(game.sequence):
            # séquence rejouée en entier : on ajoute la nouvelle couleur
            game.sequence.append(color)
            game.curr_step = 0
            game.curr_player = joueur_suivant(players, game.curr_player)
            game.turn_id += 1
            game.step_start_time = timezone.now()
        elif color == game.sequence[game.curr_step]:
            game.curr_step += 1
        else:
            erreur_couleur = True
            eliminer(game, players, game.curr_player)

        game.save()

        return None, {
            "color": color,
            "player": user.username,
            "wrong": erreur_couleur,
        }


def leave_game(code, user):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))

        if game.launched:
            for i, p in enumerate(players):
                if p.user == user and not p.eliminated:
                    eliminer(game, players, i)
            game.save()
        else:
            game.players.filter(user=user).delete()
            for i, p in enumerate(game.players.order_by("order")):
                p.order = i
                p.save()