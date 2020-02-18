import functools
from typing import Callable, List

from more_one_memo.slack import Handler
from more_one_memo.slack.model import User, Channel, ChannelID

from more_one_memo.forwarder.instance import GLOBAL_INSTANCE as GI


# Management handlers https://api.slack.com/rtm#events


def handler(event_type: str) -> Callable[[Handler], Handler]:
    """
    :return: Decorator to filter function call by type
    """

    def _handler_decorator(h: Handler) -> Handler:
        """
        :return: Function with type filter
        """

        @functools.wraps(h)
        async def filtered_handler(json: dict):
            if json['type'] == event_type:
                await h(json)

        return filtered_handler

    return _handler_decorator


# User

@handler('user_change')
async def update_user_change(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


@handler('team_join')
async def update_user_join(json: dict):
    user = User.from_json(json['user'])
    GI.users[user.id] = user


# Channel

@handler('channel_archive')
async def update_channel_archive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, True)


@handler('channel_unarchive')
async def update_channel_unarchive(json: dict):
    id_ = json['channel']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel.name, False)


@handler('channel_created')
async def update_channel_created(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    GI.channels[id_] = Channel(id_, channel_json['name'], False)


@handler('channel_deleted')
async def update_channel_deleted(json: dict):
    del GI.channels[json['channel']]


@handler('channel_rename')
async def update_channel_rename(json: dict):
    channel_json = json['channel']
    id_ = channel_json['id']
    channel = GI.channels[id_]
    GI.channels[id_] = Channel(channel.id, channel_json['name'], channel.is_archived)

# Pref


@handler('pref_change')
async def update_pref_change(json: dict):
    # https://api.slack.com/events/pref_change
    if json['name'] == 'muted_channels':
        muted_channels: List[ChannelID] = json['value'].split(',')
        GI.muted_channels = muted_channels
        return
