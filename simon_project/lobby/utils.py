import secrets, string 
from .models import Game, Player
from django.db.models import Count, Prefetch


def generate_unique_code():
    while True:
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        if not Game.objects.filter(code=code).exists():
            return code

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
