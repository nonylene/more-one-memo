"""
Slack slack.
"""
import json
import time
import traceback
import urllib.parse
import urllib.request
from typing import Optional

import websocket

from app.slack.model.model import SlackConfig

from .client import post_message


class Client:

    def __init__(self, slack_config: SlackConfig) -> None:
        self.slack_config = slack_config

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        message = "connection opened!"
        print(message)
        # post slack
        post_message(self.slack_config, message)

    def _on_close(self, ws: websocket.WebSocketApp, *close_args) -> None:
        message = "connection closed!"
        print(message)
        # post slack error
        post_message(self.slack_config, message)
        if not interrupted:
            # retry
            print("reconnecting...")
            time.sleep(2)
            self.run()

    def _on_error(self, ws: websocket.WebSocketApp, error) -> None:
        traceback.print_exc()
        # KeyboardInterrupt arrive here (0.37)
        # SystemError not arrive here (0.37~)
        if isinstance(error, SystemError) or isinstance(error, KeyboardInterrupt):
            global interrupted
            interrupted = True

    def _on_message(self, ws: websocket.WebSocketApp, message) -> None:
        message_data = json.loads(message)
        # TODO
        print(message_data)

    def run(self) -> None:
        params = urllib.parse.urlencode({'token': self.slack_config.collector_token})
        # TODO: channel info
        # TODO: user info
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
            post_message(
                self.slack_config,
                "create websocket failed: {0}".format(e)
            )
            raise


def run_client(slack_config: SlackConfig):
    client = Client(slack_config)
    client.run()
