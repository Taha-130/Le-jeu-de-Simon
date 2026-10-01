from django.db import models

from django.conf import settings
class Game(models.Model):
    code = models.CharField(max_length=6, unique=True)
    launched = models.BooleanField(default=False)
    curr_player = models.IntegerField(default=0)
    curr_step = models.IntegerField(default=0)
    step_start_time = models.DateTimeField(null=True, blank=True)
    sequence = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Salon {self.code}"
    
    
class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="players")
    order = models.IntegerField(default=0)
    eliminated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.game.code})"
