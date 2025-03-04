import re

from more_one_memo.forwarder import db
from more_one_memo.forwarder.handlers import handler
from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI
from more_one_memo.slack.model import Message

# Message handlers
# https://api.slack.com/events/message

_IGNORED_EVENTS = [
    "bot_message",
    "file_mention",
    # Hidden thread messages is represented as normal message. (2018-06-10)
    # thread_broadcast is also send as message_changed, but filtered on same text validation.
    "message_replied",
]

_SLACK_CHANNEL_PREFIX = "C"


def _get_message_url(message: Message) -> str:
    # 1582249008.070800 -> p1582249008070800
    p_ts = f"p{''.join(message.ts.split('.'))}"
    return f"https://{GI.team_domain}.slack.com/archives/{message.channel}/{p_ts}"


async def _is_shown_message(message: Message) -> bool:
    user_config = await db.get_user_config()

    if message.subtype in _IGNORED_EVENTS:
        return False

    if message.get_bot_id():
        # Slack Apps has user id and bot id both
        return False
    elif not message.get_user():
        raise ValueError(f"There is no user or bot_id in message.\nMessage: {message}")

    # Ignore groups, dms, ...
    if not message.channel.startswith(_SLACK_CHANNEL_PREFIX):
        return False
    if message.channel in user_config.ignore_channels:
        return False
    if message.get_user() in user_config.ignore_users:
        return False

    # e.g. message_changed
    if message.message is not None:
        # user is checked before
        if message.message.subtype in _IGNORED_EVENTS:
            return False

        if message.previous_message is not None:
            # Suppress attachment-orginated edits
            if message.message.text == message.previous_message.text:
                return False

    channel = GI.channels[message.channel]
    # Ignore non-muted && joined channels
    if channel.is_member and message.channel not in GI.muted_channels:
        return False
    if channel.is_member:
        for regexp in user_config.channel_regexps_member:
            if re.match(regexp, channel.name):
                return True
    else:
        for regexp in user_config.channel_regexps_nomember:
            if re.match(regexp, channel.name):
                return True

    return False  # no matched.


@handler("message")
async def handle_message(json: dict):
    message = Message.from_json(json)
    if message.get_text() is None:
        return

    if not await _is_shown_message(message):
        return

    channel = GI.channels[message.channel]
    user = GI.users[message.get_user()]  # type: ignore # user always should exist here
    message_url = _get_message_url(message)

    await GI.rest_client.post_message(
        f"`<{message_url}|#{channel.name}>` {message.get_text()}",
        GI.slack_config.post_channel,
        user.name,
        None,
        user.profile.get_image(),
    )
