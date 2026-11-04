import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Player


class SimonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.code = self.scope["url_route"]["kwargs"]["code"]
        self.group_name = f"game_{self.code}"
        self.joined = False

        user = self.scope["user"]
        if not user.is_authenticated or not await self.is_player(user):
            await self.close(code=4403)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.joined = True
        await self.accept()
        await self.broadcast_players()

    async def disconnect(self, close_code):
        if self.joined:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            await self.broadcast_players()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_json({"type": "error", "message": "JSON invalide."})
            return
        await self.send_json({"type": "error", "message": f"Type inconnu : {data.get('type')}"})

    async def players_update(self, event):
        await self.send_json({"type": "players_update", "players": event["players"]})

    async def broadcast_players(self):
        players = await self.get_players()
        await self.channel_layer.group_send(
            self.group_name, {"type": "players_update", "players": players}
        )

    async def send_json(self, payload):
        await self.send(text_data=json.dumps(payload))

    @database_sync_to_async
    def is_player(self, user):
        return Player.objects.filter(game__code=self.code, user=user).exists()

    @database_sync_to_async
    def get_players(self):
        return list(
            Player.objects.filter(game__code=self.code)
            .order_by("order")
            .values_list("user__username", flat=True)
        )