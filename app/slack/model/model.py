from typing import NamedTuple


class SlackConfig(NamedTuple):
    collector_token: str
    personal_token: str
    post_channel: str
    debug_channel: str
    default_username: str
    default_icon_emoji: str
