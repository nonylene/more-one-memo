from .handlers import handler
from .instance import GLOBAL_INSTANCE as GI
from ..slack.model import Message

# Message handlers
# https://api.slack.com/events/message

_IGNORED_EVENTS = [
    'bot_message',
    'file_mention',
    # thread messages is represented as normal message. (2018-06-10)
    'message_replied',
    'thread_broadcast',  # thread_broadcast is send as message_changed (???)
]


def _is_shown_message(message: Message) -> bool:
    if message.subtype in _IGNORED_EVENTS:
        return False
    if message.channel in GI.user_config.ignore_channels:
        return False
    if message.user in GI.user_config.ignore_users:
        return False
    if message.bot in GI.user_config.ignore_bots:
        return False

    channel = GI.channels[message.channel]
    if any(regexp.match(channel.name) for regexp in GI.filter_regexps_compiled):
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
