import traceback
import time

from motor.motor_asyncio import AsyncIOMotorClient

from more_one_memo.slack import WebSocketClient, RestClient

from more_one_memo.forwarder import handlers, instance, db
from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI
from more_one_memo.forwarder.message_handler import handle_message
from more_one_memo.forwarder.model import ForwarderConfig

_HANDLERS = [
    # Management
    handlers.update_user_change,
    handlers.update_user_join,
    handlers.update_channel_archive,
    handlers.update_channel_unarchive,
    handlers.update_channel_created,
    handlers.update_channel_deleted,
    handlers.update_channel_rename,
    handlers.update_channel_left,
    handlers.update_member_joined_channel,
    handlers.update_pref_change,
    # Message
    handle_message,
]


async def _logger(text: str):
    print(text)
    await GI.rest_client.post_message(
        text,
        GI.slack_config.debug_channel,
        GI.slack_config.default_username,
        GI.slack_config.default_icon_emoji,
        None
    )


async def run(forwarder_config: ForwarderConfig):
    poster_rest_client = RestClient(forwarder_config.poster_token)
    collector_rest_client = RestClient(forwarder_config.collector_token)

    # Init
    # We need to use rtm.start to get muted channels.
    rtm_start = await poster_rest_client.rtm_start()
    instance.init(
        forwarder_config,
        AsyncIOMotorClient(forwarder_config.mongo_uri),
        poster_rest_client,
        rtm_start.team.domain,
        rtm_start.self_.id,
        dict((user.id, user) for user in rtm_start.users),
        dict((channel.id, channel) for channel in rtm_start.channels),
        rtm_start.self_.prefs.muted_channels
    )
    del rtm_start

    await db.init_db()

    try:
        while True:
            rtm_connect = await collector_rest_client.rtm_connect()

            try:
                websocket_client = WebSocketClient(_logger, _HANDLERS)
                await websocket_client.run(rtm_connect.url)
            except WebSocketClient.ConenctionClosedError:
                traceback.print_exc()
                # Retry
                print("Reconnecting...")
                time.sleep(2)
                continue

    except Exception as e:
        await _logger("Failed to create websocket: {0}".format(e))
        raise
