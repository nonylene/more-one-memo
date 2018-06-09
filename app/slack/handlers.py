import functools
from typing import Callable

from .client import Handler
from .client.model import User, Channel
from .instance import GLOBAL_INSTANCE as GI


# https://api.slack.com/rtm#events


def _handler(event_type: str) -> Callable[[Handler], Handler]:
    """
    :return: decorator to filter function call by type
    """

    def _handler_decorator(handler: Handler) -> Handler:
        """
        :return: function with type filter
        """

        @functools.wraps(handler)
        def filtered_handler(json: dict):
            if json['type'] == event_type:
                handler(json)

        return filtered_handler

    return _handler_decorator


# User

@_handler('user_change')
def update_user_change(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


@_handler('team_join')
def update_user_join(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


@_handler('bot_changed')
def update_bot_change(json: dict):
    user = User.from_json(json['bot'])
    GI.users[user.id] = user


@_handler('bot_added')
def update_bot_add(json: dict):
    user = User.from_json(json['bot'])
    GI.users[user.id] = user


# Channel

@_handler('channel_archive')
def update_channel_archive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, True)


@_handler('channel_unarchive')
def update_channel_unarchive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, False)


@_handler('channel_created')
def update_channel_created(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    GI.channels[id_] = Channel(id_, channel_json['name'], False)


@_handler('channel_deleted')
def update_channel_deleted(json: dict):
    del GI.channels[json['channel']]


@_handler('channel_rename')
def update_channel_rename(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel_json['name'], channel.is_archived)
