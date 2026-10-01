import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SimonConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "connection",
            "message": "Connexion WebSocket établie avec Simon Online",
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Le message reçu n'est pas un JSON valide.",
            }))
            return

        await self.send(text_data=json.dumps({
            "type": "echo",
            "message": "Message reçu par le serveur.",
            "data": data,
        }))
