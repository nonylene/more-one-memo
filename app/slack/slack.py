from .client import WebSocketClient, RestClient
from .instance import INSTANCE as I
from .instance import init
from .model import SlackConfig


def _logger(text: str):
    print(text)
    I.rest_client.post_message(
        text,
        I.rest_client.debug_channel,
        I.slack_config.default_username,
        I.slack_config.default_icon_emoji
    )


def run_client(slack_config: SlackConfig):
    rest_client = RestClient(slack_config.personal_token)

    init(
        slack_config,
        rest_client,
        dict((user.id, user) for user in rest_client.get_users()),
        dict((channel.id, channel) for channel in rest_client.get_channels()),
    )

    websocket_client = WebSocketClient(slack_config.collector_token, _logger)
    websocket_client.run()
