from dataclasses import dataclass


@dataclass
class ForwarderConfig:
    mongo_uri: str
    collector_token: str
    poster_token: str
    post_channel: str
    debug_channel: str
    default_username: str
    default_icon_emoji: str
