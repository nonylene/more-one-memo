from typing import Dict

from .client import RestClient
from .client.model import User, Channel, UserID, ChannelID
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
        self.channels: Dict[ChannelID, Channel] = None


GLOBAL_INSTANCE: Instance = Instance()


def init(
        slack_config: SlackConfig, rest_client: RestClient,
        users: Dict[UserID, User], channels: Dict[ChannelID, Channel]
):
    GLOBAL_INSTANCE.slack_config = slack_config
    GLOBAL_INSTANCE.rest_client = rest_client
    GLOBAL_INSTANCE.users = users
    GLOBAL_INSTANCE.channels = channels
