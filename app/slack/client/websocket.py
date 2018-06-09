"""
Slack slack.
"""
import json
import time
import traceback
import urllib.parse
import urllib.request
from typing import Callable, List

import websocket

Handler = Callable[[dict], None]


class WebSocketClient:

    def __init__(self, token: str, logger: Callable[[str], None], handlers: List[Handler]) -> None:
        self.token = token
        self.logger = logger
        self.handlers = handlers

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        self.logger("Connection opened!")

    def _on_close(self, ws: websocket.WebSocketApp, *close_args) -> None:
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
        params = urllib.parse.urlencode({'token': self.token})
        try:
            start_api = "https://slack.com/api/rtm.connect?{0}".format(params)
            res = urllib.request.urlopen(start_api)
            start_data = json.loads(res.read().decode())
            websocket_url = start_data["url"]
            # websocket.enableTrace(True)
            ws = websocket.WebSocketApp(
                websocket_url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_open=self._on_open,
                on_close=self._on_close
            )

            ws.run_forever()

        except Exception as e:
            traceback.print_exc()
            self.logger("Create websocket failed: {0}".format(e))
            raise
