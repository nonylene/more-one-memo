import functools
from typing import Callable

from more_one_memo.slack import Handler
from more_one_memo.slack.model import User, Channel

from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI


# Management handlers https://api.slack.com/rtm#events


def handler(event_type: str) -> Callable[[Handler], Handler]:
    """
    :return: decorator to filter function call by type
    """

    def _handler_decorator(h: Handler) -> Handler:
        """
        :return: function with type filter
        """

        @functools.wraps(h)
        def filtered_handler(json: dict):
            if json['type'] == event_type:
                h(json)

        return filtered_handler

    return _handler_decorator


# User

@handler('user_change')
def update_user_change(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


@handler('team_join')
def update_user_join(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


@handler('bot_changed')
def update_bot_change(json: dict):
    user = User.from_json(json['bot'])
    GI.users[user.id] = user


@handler('bot_added')
def update_bot_add(json: dict):
    user = User.from_json(json['bot'])
    GI.users[user.id] = user


# Channel

@handler('channel_archive')
def update_channel_archive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, True)


@handler('channel_unarchive')
def update_channel_unarchive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, False)


@handler('channel_created')
def update_channel_created(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    GI.channels[id_] = Channel(id_, channel_json['name'], False)


@handler('channel_deleted')
def update_channel_deleted(json: dict):
    del GI.channels[json['channel']]


@handler('channel_rename')
def update_channel_rename(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel_json['name'], channel.is_archived)
