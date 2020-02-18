import json
from typing import Callable, List, Awaitable

# import websocket
import websockets

Handler = Callable[[dict], Awaitable[None]]


class WebSocketClient:

    class ConenctionClosedError(Exception):
        pass

    def __init__(self, logger: Callable[[str], Awaitable[None]], handlers: List[Handler]) -> None:
        self.logger = logger
        self.handlers = handlers

    async def _notify_open(self) -> None:
        await self.logger("Connection opened!")

    async def _notify_close(self) -> None:
        await self.logger("Connection closed!")

    async def _on_message(self, message: str) -> None:
        message_data = json.loads(message)
        print(message_data)  # TODO: debug
        for handler in self.handlers:
            await handler(message_data)

    async def run(self, url: str) -> None:
        try:
            async with websockets.connect(url) as websocket:
                await self._notify_open()
                async for message in websocket:
                    await self._on_message(message)
        except websockets.exceptions.ConnectionClosed as e:
            await self._notify_close()
            raise self.ConenctionClosedError from e
