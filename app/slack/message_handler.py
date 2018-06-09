from .client.model import Message
from .handlers import handler
from .instance import GLOBAL_INSTANCE as GI

# Message handlers
# https://api.slack.com/events/message

_IGNORED_EVENTS = [
    'bot_message',
    'file_mention',
    # thread messages is represented as normal message. (2018-06-10)
    'message_replied',
    'thread_broadcast',  # thread_broadcast is send as message_changed (???)
]


@handler('message')
def handle_message(json: dict):
    message = Message.from_json(json)
    if message.subtype in _IGNORED_EVENTS:
        return
    if message.text is None:
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
