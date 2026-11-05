import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from . import game_logic
from .models import Player


class SimonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.code = self.scope["url_route"]["kwargs"]["code"]
        self.group_name = "game_" + self.code

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.envoyer_joueurs()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        if data.get("type") == "start":
            await self.lancer_partie()
        if data.get("type") == "color":
            await self.jouer_couleur(data.get("color"))

    async def lancer_partie(self):
        erreur, pseudo = await database_sync_to_async(game_logic.start_game)(
            self.code, 
            self.scope["user"]
        )
        if erreur:
            await self.send(text_data=json.dumps({
                "type": "error", 
                "message": erreur
            }))
            return

        await self.channel_layer.group_send(
            self.group_name, {
                "type": "game_started",
                "player": pseudo,
            }
        )

    async def game_started(self, event):
        await self.send(text_data=json.dumps({
            "type": "game_started",
            "player": event["player"],
        }))

    async def envoyer_joueurs(self):
        joueurs = await self.get_joueurs()
        await self.channel_layer.group_send(self.group_name, {
            "type": "players_update",
            "players": joueurs,
        })

    async def players_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "players_update",
            "players": event["players"],
        }))
        
    async def jouer_couleur(self, couleur):
        erreur, resultat = await database_sync_to_async(game_logic.play_color)(
            self.code, self.scope["user"], couleur
        )
        if erreur:
            await self.send(text_data=json.dumps({"type": "error", "message": erreur}))
            return

        resultat["type"] = "color_played"
        await self.channel_layer.group_send(self.group_name, resultat)

    async def color_played(self, event):
        await self.send(text_data=json.dumps({
            "type": "color_played",
            "color": event["color"],
            "player": event["player"],
            "wrong": event["wrong"],
            "next": event["next"],
        }))

    @database_sync_to_async
    def get_joueurs(self):
        return list(
            Player.objects.filter(game__code=self.code)
            .order_by("order")
            .values_list("user__username", flat=True)
        )