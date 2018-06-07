import json
import time
import traceback
import urllib.parse
import urllib.request
from typing import Optional

from .model import SlackConfig


def post_message(
        slack_config: SlackConfig,
        text: str,
        channel: Optional[str] = None, username: Optional[str] = None, icon_emoji: Optional[str] = None,
) -> None:
    if channel is None:
        channel = slack_config.debug_channel
    if username is None:
        username = slack_config.default_username
    if icon_emoji is None:
        icon_emoji = slack_config.default_icon_emoji

    data = {
        "token": slack_config.personal_token,
        "channel": channel,
        "text": text,
        "icon_emoji": icon_emoji,
        "username": username
    }
    post_data = urllib.parse.urlencode(data).encode()
    urllib.request.urlopen(
        "https://slack.com/api/chat.postMessage",
        data=post_data
    )
