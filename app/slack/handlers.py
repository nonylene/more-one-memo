import functools
from typing import Callable

from .client import Handler
from .client.model import User, Channel
from .instance import INSTANCE as I

"""
https://api.slack.com/rtm#events
"""


def _handler(type: str) -> Callable[[Handler], Handler]:
    """
    :return: decorator to filter function call by type
    """

    def _handler_decorator(handler: Callable[[dict], None]) -> Callable[[dict], None]:
        """
        :return: function with type filter
        """

        @functools.wraps(handler)
        def filtered_handler(json: dict):
            if json['type'] == type:
                handler(json)

        return filtered_handler

    return _handler_decorator


## User

@_handler('user_change')
def update_user_change(json: dict):
    user = User.from_json(json['user'])
    I.users[user.id] = user


@_handler('team_join')
def update_user_join(json: dict):
    user = User.from_json(json['user'])
    I.users[user.id] = user


## Channel

@_handler('channel_archive')
def update_channel_archive(json: dict):
    id = json['channel']
    channel = I.channels[id]
    I.channels[id] = Channel(channel.id, channel.name, True)


@_handler('channel_unarchive')
def update_channel_unarchive(json: dict):
    id = json['channel']
    channel = I.channels[id]
    I.channels[id] = Channel(channel.id, channel.name, False)


@_handler('channel_created')
def update_channel_created(json: dict):
    channel_json = json['channel']
    id = channel_json['id']
    I.channels[id] = Channel(id, channel_json['name'], False)


@_handler('channel_deleted')
def update_channel_deleted(json: dict):
    del I.channels[json['channel']]


@_handler('channel_rename')
def update_channel_rename(json: dict):
    channel_json = json['channel']
    id = channel_json['id']
    channel = I.channels[id]
    I.channels[id] = Channel(channel.id, channel_json['name'], channel.is_archived)
