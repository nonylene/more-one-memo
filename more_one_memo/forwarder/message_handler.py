import re

from more_one_memo.slack.model import Message

from more_one_memo.forwarder import db
from more_one_memo.forwarder.handlers import handler
from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI

# Message handlers
# https://api.slack.com/events/message

_IGNORED_EVENTS = [
    'bot_message',
    'file_mention',
    # thread messages is represented as normal message. (2018-06-10)
    'message_replied',
    'thread_broadcast',  # thread_broadcast is send as message_changed (???)
]

_SLACK_CHANNEL_PREFIX = 'C'


def _is_shown_message(message: Message) -> bool:
    user_config = db.get_user_config()

    if message.subtype in _IGNORED_EVENTS:
        return False
    # Ignore groups, dms, ...
    if not message.channel.startswith(_SLACK_CHANNEL_PREFIX):
        return False
    if message.channel in user_config.ignore_channels:
        return False
    if message.user in user_config.ignore_users:
        return False
    if message.bot in user_config.ignore_bots:
        return False

    channel = GI.channels[message.channel]
    for regexp in user_config.channel_regexps:
        if re.match(regexp, channel.name):
            return True

    return False  # no matched.


@handler('message')
def handle_message(json: dict):
    message = Message.from_json(json)
    if message.text is None:
        return

    if not _is_shown_message(message):
        return

    channel = GI.channels[message.channel]
    user = GI.users[message.user]

    GI.rest_client.post_message(
        f'`{channel.get_link()}` {message.text}',
        GI.slack_config.post_channel,
        user.name,
        None,
        user.profile.image_72
    )
