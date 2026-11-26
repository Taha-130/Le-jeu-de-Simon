import asyncio
from collections.abc import Awaitable, Callable

ACTIVE_TIMERS = {}

def cancel_timer(game_code):
    task = ACTIVE_TIMERS.pop(game_code, None)
    if task and not task.done():
        task.cancel()

def start_timer(game_code, turn_id, duration, on_timeout):
    """
    Start timer for a given turn (cancelling old one if still running)
    """
    cancel_timer(game_code)

    async def _countdown():
        try:
            await asyncio.sleep(duration)
            await on_timeout(game_code, turn_id)
        except asyncio.CancelledError:
            pass
    
    ACTIVE_TIMERS[game_code] = asyncio.create_task(_countdown())