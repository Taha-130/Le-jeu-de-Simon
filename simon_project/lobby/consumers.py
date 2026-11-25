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
        await self.send_players()
        await self.envoyer_etat()

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
            await self.start_game()
        if data.get("type") == "color":
            await self.play_color(data.get("color"))

    # --- players actions ---
    async def start_game(self):
        error, pseudo = await database_sync_to_async(game_logic.start_game)(
            self.code, self.scope["user"]
        )
        if error:
            await self.send(text_data=json.dumps({"type": "error", "message": error}))
            return

        await self.channel_layer.group_send(self.group_name, {
            "type": "game_started",
            "player": pseudo,
        })

    async def play_color(self, color):
        error, resultat = await database_sync_to_async(game_logic.play_color)(
            self.code, self.scope["user"], color
        )
        if error:
            await self.send(text_data=json.dumps({"type": "error", "message": error}))
            return

        resultat["type"] = "color_played"
        await self.channel_layer.group_send(self.group_name, resultat)

        etat = await database_sync_to_async(game_logic.get_state)(self.code)
        await self.channel_layer.group_send(self.group_name, {
            "type": "state_update",
            "state": etat,
        })

    # --- info sent to browsers ---
    async def send_players(self):
        players = await self.get_players()
        await self.channel_layer.group_send(self.group_name, {
            "type": "players_update",
            "players": players,
        })

    async def envoyer_etat(self):
        etat = await database_sync_to_async(game_logic.get_state)(self.code)
        if etat:
            await self.send(text_data=json.dumps({"type": "state", **etat}))

    async def players_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "players_update",
            "players": event["players"],
        }))

    async def game_started(self, event):
        await self.send(text_data=json.dumps({
            "type": "game_started",
            "player": event["player"],
        }))

    async def color_played(self, event):
        await self.send(text_data=json.dumps({
            "type": "color_played",
            "color": event["color"],
            "player": event["player"],
            "wrong": event["wrong"],
        }))

    async def state_update(self, event):
        await self.send(text_data=json.dumps({"type": "state", **event["state"]}))

    @database_sync_to_async
    def get_players(self):
        return list(
            Player.objects.filter(game__code=self.code)
            .order_by("order")
            .values_list("user__username", flat=True)
        )