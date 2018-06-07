from typing import Dict

from .client import RestClient
from .client.model import User, Channel
from .model import SlackConfig


class Instance:
    """
    Class for keeping global variable.
    """

    def __init__(self):
        """
        :param slack_config:
        :param rest_client:
        :param users: Dictionary of id and Channel object
        :param channels: Dictionary of id and Channel object
        """
        self.slack_config: SlackConfig = None
        self.rest_client: RestClient = None
        self.users: Dict[str, User] = None
        self.channels: Dict[str, Channel] = None


INSTANCE: Instance = Instance()


def init(
        slack_config: SlackConfig, rest_client: RestClient,
        users: Dict[str, User], channels: Dict[str, Channel]
):
    INSTANCE.slack_config = slack_config
    INSTANCE.rest_client = rest_client
    INSTANCE.users = users
    INSTANCE.channels = channels
