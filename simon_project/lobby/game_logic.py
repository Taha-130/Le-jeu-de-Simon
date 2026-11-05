from django.db import transaction
from django.utils import timezone
from .models import Game

COULEURS = ["rouge", "bleu", "vert", "jaune"]

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
    
def joueur_suivant(players, actuel):
    n = len(players)
    for i in range(1, n + 1):
        index = (actuel + i) % n
        if not players[index].eliminated:
            return index
    return actuel


def play_color(code, user, color):      
    if color not in COULEURS:
        return "Couleur invalide.", None

    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))

        if not game.launched:
            return "La partie n'a pas commencé.", None
        if players[game.curr_player].user != user:
            return "Ce n'est pas ton tour.", None

        erreur_couleur = False

        if game.curr_step == len(game.sequence):
            # séquence est rejouée en entier : ajout nouvelle couleur
            game.sequence.append(color)
            game.curr_step = 0
            game.curr_player = joueur_suivant(players, game.curr_player)
            game.turn_id += 1
            game.step_start_time = timezone.now()
        elif color == game.sequence[game.curr_step]:
            game.curr_step += 1
        else:
            erreur_couleur = True

        game.save()

        return None, {
            "color": color,
            "player": user.username,
            "wrong": erreur_couleur,
            "next": players[game.curr_player].user.username,
        }