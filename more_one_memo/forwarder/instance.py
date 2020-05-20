from typing import Dict, List

from motor.motor_asyncio import AsyncIOMotorClient

from more_one_memo.slack import RestClient
from more_one_memo.slack.model import User, Channel, UserID, ChannelID

from more_one_memo.forwarder.model import ForwarderConfig


class Instance:
    """
    Class for keeping global variable.
    :users: Dictionary of id and Channel object
    :channels: Dictionary of id and Channel object
    """
    slack_config: ForwarderConfig
    mongo_client: AsyncIOMotorClient
    rest_client: RestClient
    team_domain: str
    user_id: UserID
    users: Dict[UserID, User]
    channels: Dict[ChannelID, Channel]
    muted_channels: List[ChannelID]


GLOBAL_INSTANCE: Instance = Instance()


def init(
        slack_config: ForwarderConfig,
        mongo_client: AsyncIOMotorClient, rest_client: RestClient,
        team_domain: str, user_id: str,
        users: Dict[UserID, User], channels: Dict[ChannelID, Channel], muted_channels: List[ChannelID]
):
    GLOBAL_INSTANCE.slack_config = slack_config
    GLOBAL_INSTANCE.mongo_client = mongo_client
    GLOBAL_INSTANCE.rest_client = rest_client
    GLOBAL_INSTANCE.team_domain = team_domain
    GLOBAL_INSTANCE.user_id = user_id
    GLOBAL_INSTANCE.users = users
    GLOBAL_INSTANCE.channels = channels
    GLOBAL_INSTANCE.muted_channels = muted_channels
