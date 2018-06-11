from google.cloud import datastore

from . import handlers
from .client import WebSocketClient, RestClient
from .instance import GLOBAL_INSTANCE as GI
from .instance import init, set_user_config
from .message_handler import handle_message
from .model import SlackConfig
from ..data import get_config
from ..data.model import DatastoreConfig

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
    # Message
    handle_message,
]

_DATASTORE_CLIENT = datastore.Client()
_DATASTORE_CONFIG: DatastoreConfig = None


def _logger(text: str):
    print(text)
    GI.rest_client.post_message(
        text,
        GI.slack_config.debug_channel,
        GI.slack_config.default_username,
        GI.slack_config.default_icon_emoji,
        None
    )


def run_client(datastore_config: DatastoreConfig, slack_config: SlackConfig):
    global _DATASTORE_CONFIG
    _DATASTORE_CONFIG = datastore_config

    load_user_config()

    rest_client = RestClient(slack_config.personal_token)
    rtm_start = rest_client.rtm_start()

    init(
        slack_config,
        rest_client,
        dict((user.id, user) for user in rtm_start.users),
        dict((bot.id, bot) for bot in rtm_start.bots),
        dict((channel.id, channel) for channel in rtm_start.channels),
        rtm_start.self_.prefs.muted_channels
    )

    websocket_client = WebSocketClient(rtm_start.url, _logger, _HANDLERS)
    websocket_client.run()


def load_user_config():
    set_user_config(get_config(_DATASTORE_CLIENT, _DATASTORE_CONFIG))
