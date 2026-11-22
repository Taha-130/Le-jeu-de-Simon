from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer


@shared_task
def test_task(code):
    async_to_sync(get_channel_layer().group_send)("game_" + code, {
        "type": "players_update",
        "players": ["test_celery"],
    })