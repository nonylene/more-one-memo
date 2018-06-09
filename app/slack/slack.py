from . import handlers
from .client import WebSocketClient, RestClient
from .instance import INSTANCE as I
from .instance import init
from .model import SlackConfig

_HANDLERS = [
    # Management
    handlers.update_user_change,
    handlers.update_user_join,
    handlers.update_bot_add,
    handlers.update_bot_change,
    handlers.update_channel_archive,
    handlers.update_channel_unarchive,
    handlers.update_channel_created,
    handlers.update_channel_deleted,
    handlers.update_channel_rename,
]


def _logger(text: str):
    print(text)
    I.rest_client.post_message(
        text,
        I.slack_config.debug_channel,
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

    websocket_client = WebSocketClient(slack_config.collector_token, _logger, _HANDLERS)
    websocket_client.run()
