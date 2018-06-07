from typing import List, Dict

from .client import RestClient
from .client.model import User, Channel
from .model import SlackConfig


class Instance:
    """
    Class for keeping global variable.
    """

    def __init__(self,
                 slack_config: SlackConfig, rest_client: RestClient,
                 users: Dict[str, User], channels: Dict[str, Channel]
                 ):
        """
        :param slack_config:
        :param rest_client:
        :param users: Dictionary of id and Channel object
        :param channels: Dictionary of id and Channel object
        """
        self.slack_config = slack_config
        self.rest_client = rest_client
        self.users = users
        self.channels = channels


INSTANCE: Instance = None

def set_instance(instance: Instance):
    global INSTANCE
    INSTANCE = instance
