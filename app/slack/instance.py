from typing import Dict, List

from .client import RestClient
from .client.model import User, Channel, UserID, ChannelID, Bot, BotID
from .model import SlackConfig


class Instance:
    """
    Class for keeping global variable.
    """

    def __init__(self):
        """
        :slack_config:
        :rest_client:
        :users: Dictionary of id and Channel object
        :channels: Dictionary of id and Channel object
        """
        self.slack_config: SlackConfig = None
        self.rest_client: RestClient = None
        self.users: Dict[UserID, User] = None
        self.bots: Dict[BotID, Bot]
        self.channels: Dict[ChannelID, Channel] = None
        self.muted_channels: List[ChannelID] = None


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
