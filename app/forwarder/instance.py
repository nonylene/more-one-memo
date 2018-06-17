import re
from typing import Dict, List, Pattern

from .model import SlackConfig
from ..model import UserConfig
from ..slack import RestClient
from ..slack.model import User, Channel, UserID, ChannelID, Bot, BotID


class Instance:
    """
    Class for keeping global variable.
    :slack_config:
    :rest_client:
    :users: Dictionary of id and Channel object
    :channels: Dictionary of id and Channel object
    """
    user_config: UserConfig
    filter_regexps_compiled: List[Pattern]

    slack_config: SlackConfig
    rest_client: RestClient
    users: Dict[UserID, User]
    bots: Dict[BotID, Bot]
    channels: Dict[ChannelID, Channel]
    muted_channels: List[ChannelID]


GLOBAL_INSTANCE: Instance = Instance()


def init(
        slack_config: SlackConfig, rest_client: RestClient,
        users: Dict[UserID, User], bots: Dict[BotID, Bot],
        channels: Dict[ChannelID, Channel], muted_channels: List[ChannelID]
):
    GLOBAL_INSTANCE.slack_config = slack_config
    GLOBAL_INSTANCE.rest_client = rest_client
    GLOBAL_INSTANCE.users = users
    GLOBAL_INSTANCE.bots = bots
    GLOBAL_INSTANCE.channels = channels
    GLOBAL_INSTANCE.muted_channels = muted_channels


def set_user_config(user_config: UserConfig):
    GLOBAL_INSTANCE.user_config = user_config
    GLOBAL_INSTANCE.filter_regexps_compiled = [re.compile(regexp) for regexp in user_config.filter_regexps]
