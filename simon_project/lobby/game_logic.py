from django.db import transaction
from django.utils import timezone
from .models import Game
from datetime import timedelta

COLORS = ["red", "blue", "green", "yellow"]


def next_player(players, current):
    n = len(players)
    for i in range(1, n + 1):
        index = (current + i) % n
        if not players[index].eliminated:
            return index
    return current


def eliminate(game, players, index):
    players[index].eliminated = True
    players[index].save()

    alive_players = [p for p in players if not p.eliminated]
    if len(alive_players) > 1 and game.curr_player == index:
        game.curr_player = next_player(players, index)
        game.curr_step = 0
        game.turn_id += 1
        game.step_start_time = timezone.now()

    # only one player left: the game is over, record the winner
    if len(alive_players) == 1 and game.winner is None:
        game.winner = alive_players[0].user


def get_state(code):
    game = Game.objects.filter(code=code).first()
    if game is None:
        return None
    players = list(game.players.order_by("order"))
    alive_players = [p for p in players if not p.eliminated]

    winner = None
    if game.launched and len(players) > 1 and len(alive_players) == 1:
        winner = alive_players[0].user.username

    current = None
    if game.launched and players:
        current = players[game.curr_player].user.username

    return {
        "launched": game.launched,
        "current": current,
        "winner": winner,
        "length": len(game.sequence),
        "players": [
            {
                "name": p.user.username,
                "eliminated": p.eliminated,
                "turns": p.successful_turns,
                "best": p.longest_sequence,
            }
            for p in players
        ],
    }


def start_game(code, user):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))

        if game.launched:
            return "The game has already started.", None
        if not players or players[0].user != user:
            return "Only the creator of the room can start the game.", None
        if len(players) < 2:
            return "At least 2 players are required.", None

        game.launched = True
        game.sequence = []
        game.curr_player = 0
        game.curr_step = 0
        game.turn_id += 1
        game.step_start_time = timezone.now()
        game.save()

        return None, players[0].user.username


def play_color(code, user, color):
    if color not in COLORS:
        return "Invalid color.", None

    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))
        alive_players = [p for p in players if not p.eliminated]

        if not game.launched:
            return "The game has not started yet.", None
        if len(alive_players) <= 1:
            return "The game is over.", None
        if players[game.curr_player].user != user:
            return "It's not your turn.", None

        wrong_color = False

        if game.curr_step == len(game.sequence):
            # the player repeated the whole sequence and adds a new color
            game.sequence.append(color)

            # record this successful turn for the current player
            player = players[game.curr_player]
            player.successful_turns += 1
            player.longest_sequence = max(player.longest_sequence, len(game.sequence))
            player.save()

            game.curr_step = 0
            game.curr_player = next_player(players, game.curr_player)
            game.turn_id += 1
            game.step_start_time = timezone.now()
            
        elif color == game.sequence[game.curr_step]:
            game.curr_step += 1
        else:
            wrong_color = True
            eliminate(game, players, game.curr_player)

        game.save()

        return None, {
            "color": color,
            "player": user.username,
            "wrong": wrong_color,
        }


def leave_game(code, user):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(code=code)
        players = list(game.players.order_by("order"))

        if game.launched:
            for i, p in enumerate(players):
                if p.user == user and not p.eliminated:
                    eliminate(game, players, i)
            game.save()
        else:
            game.players.filter(user=user).delete()
            for i, p in enumerate(game.players.order_by("order")):
                p.order = i
                p.save()


def get_turn_timer(code):
    game = Game.objects.filter(code=code, launched=True).first()
    if (game is None) or (game.players.filter(eliminated=False).count() <= 1):
        return None     # no game found or no alive players anymore
    return game.turn_id, game.turn_duration


def expire_turn(code, expected_turn_id):
    with transaction.atomic():
        game = Game.objects.select_for_update().filter(code=code).first()
        if (
            game is None    # no game found
            or not game.launched
            or game.turn_id != expected_turn_id
            or game.step_start_time is None
            or timezone.now() < game.step_start_time + timedelta(seconds=game.turn_duration)
        ):
            return False

        players = list(game.players.order_by("order"))
        if sum(not player.eliminated for player in players) <= 1:
            return False    # game already ended

        eliminate(game, players, game.curr_player)
        game.save()
        return True
