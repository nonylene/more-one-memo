from typing import Dict, List

from pymongo import MongoClient

from more_one_memo.slack import RestClient
from more_one_memo.slack.model import User, Channel, UserID, ChannelID, Bot, BotID

from more_one_memo.forwarder.model import ForwarderConfig


class Instance:
    """
    Class for keeping global variable.
    :users: Dictionary of id and Channel object
    :channels: Dictionary of id and Channel object
    """
    slack_config: ForwarderConfig
    mongo_client: MongoClient
    rest_client: RestClient
    users: Dict[UserID, User]
    bots: Dict[BotID, Bot]
    channels: Dict[ChannelID, Channel]
    muted_channels: List[ChannelID]


GLOBAL_INSTANCE: Instance = Instance()


def init(
        slack_config: ForwarderConfig,
        mongo_client: MongoClient, rest_client: RestClient,
        users: Dict[UserID, User], bots: Dict[BotID, Bot],
        channels: Dict[ChannelID, Channel], muted_channels: List[ChannelID]
):
    GLOBAL_INSTANCE.slack_config = slack_config
    GLOBAL_INSTANCE.mongo_client = mongo_client
    GLOBAL_INSTANCE.rest_client = rest_client
    GLOBAL_INSTANCE.users = users
    GLOBAL_INSTANCE.bots = bots
    GLOBAL_INSTANCE.channels = channels
    GLOBAL_INSTANCE.muted_channels = muted_channels
