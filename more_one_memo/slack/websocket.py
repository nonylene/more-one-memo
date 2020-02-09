import json
import time
import traceback
from typing import Callable, List

import websocket

Handler = Callable[[dict], None]


class WebSocketClient:

    def __init__(self, url: str, logger: Callable[[str], None], handlers: List[Handler]) -> None:
        self.url = url
        self.logger = logger
        self.handlers = handlers

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        self.logger("Connection opened!")

    def _on_close(self, ws: websocket.WebSocketApp) -> None:
        self.logger("Connection closed!")
        if not interrupted:
            # retry
            self.logger("Reconnecting...")
            time.sleep(2)
            self.run()

    def _on_error(self, ws: websocket.WebSocketApp, error: BaseException) -> None:
        traceback.print_exc()
        # KeyboardInterrupt arrive here (0.37)
        # SystemExit not arrive here (0.37~)
        if isinstance(error, SystemExit) or isinstance(error, KeyboardInterrupt):
            global interrupted
            interrupted = True

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        message_data = json.loads(message)
        print(message_data)  # TODO: debug
        for handler in self.handlers:
            # We must handle exception here because that occurred in callback does not thrown outer.
            try:
                handler(message_data)
            except Exception as e:
                traceback.print_exc()
                self.logger('Exception occurred: {0}'.format(e))

    def run(self) -> None:
        # https://api.slack.com/methods/rtm.start
        ws = websocket.WebSocketApp(
            self.url,
            on_message=lambda ws, msg: self._on_message(ws, msg),
            on_error=lambda ws, error: self._on_error(ws, error),
            on_open=lambda ws: self._on_open(ws),
            on_close=lambda ws: self._on_close(ws),
        )
        ws.run_forever()
