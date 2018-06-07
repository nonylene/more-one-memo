from typing import List

from .client import WebSocketClient, RestClient
from .model import SlackConfig, User, Channel

_SLACK_CONFIG: SlackConfig
_REST_CLIENT: RestClient

_USERS: List[User]
_CHANNELS: List[Channel]


def _logger(text: str):
    print(text)
    _REST_CLIENT.post_message(
        text,
        _SLACK_CONFIG.debug_channel,
        _SLACK_CONFIG.default_username,
        _SLACK_CONFIG.default_icon_emoji
    )


def run_client(slack_config: SlackConfig):
    global _SLACK_CONFIG
    _SLACK_CONFIG = slack_config

    global _REST_CLIENT
    _REST_CLIENT = RestClient(slack_config.personal_token)

    global _USERS
    _USERS = _REST_CLIENT.get_users()

    global _CHANNELS
    _CHANNELS = _REST_CLIENT.get_channels()

    websocket_client = WebSocketClient(slack_config.collector_token, _logger)
    websocket_client.run()
