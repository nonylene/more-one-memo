from typing import List, NamedTuple

from .client import WebSocketClient, RestClient
from .client.model import User, Channel


class SlackConfig(NamedTuple):
    collector_token: str
    personal_token: str
    post_channel: str
    debug_channel: str
    default_username: str
    default_icon_emoji: str


SLACK_CONFIG: SlackConfig
REST_CLIENT: RestClient

USERS: List[User]
CHANNELS: List[Channel]


def _logger(text: str):
    print(text)
    REST_CLIENT.post_message(
        text,
        SLACK_CONFIG.debug_channel,
        SLACK_CONFIG.default_username,
        SLACK_CONFIG.default_icon_emoji
    )


def run_client(slack_config: SlackConfig):
    global SLACK_CONFIG
    SLACK_CONFIG = slack_config

    global REST_CLIENT
    REST_CLIENT = RestClient(slack_config.personal_token)

    global USERS
    USERS = REST_CLIENT.get_users()

    global CHANNELS
    CHANNELS = REST_CLIENT.get_channels()

    websocket_client = WebSocketClient(slack_config.collector_token, _logger)
    websocket_client.run()
