from pymongo import MongoClient

from more_one_memo.slack import WebSocketClient, RestClient

from more_one_memo.forwarder import handlers, instance, db
from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI
from more_one_memo.forwarder.message_handler import handle_message
from more_one_memo.forwarder.model import ForwarderConfig

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


def _logger(text: str):
    print(text)
    GI.rest_client.post_message(
        text,
        GI.slack_config.debug_channel,
        GI.slack_config.default_username,
        GI.slack_config.default_icon_emoji,
        None
    )


def run(slack_config: ForwarderConfig):
    rest_client = RestClient(slack_config.poster_token)
    rtm_start = rest_client.rtm_start()

    instance.init(
        slack_config,
        MongoClient(slack_config.mongo_uri),
        rest_client,
        dict((user.id, user) for user in rtm_start.users),
        dict((bot.id, bot) for bot in rtm_start.bots),
        dict((channel.id, channel) for channel in rtm_start.channels),
        rtm_start.self_.prefs.muted_channels
    )

    db.init_db()

    websocket_client = WebSocketClient(rtm_start.url, _logger, _HANDLERS)
    websocket_client.run()
