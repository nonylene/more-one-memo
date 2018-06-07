from typing import NamedTuple
from google.cloud import datastore


class UserConfig(NamedTuple):
    id: str

    @staticmethod
    def from_entity(entity: datastore.Entity):
        return UserConfig(entity["id"])


class SlackConfig(NamedTuple):
    collector_token: str
    personal_token: str
    post_channel: str
    debug_channel: str
    default_username: str
    default_icon_emoji: str
