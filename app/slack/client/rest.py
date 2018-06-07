import json
import urllib.parse
import urllib.request
from typing import Optional

from ..model import SlackConfig, Channel, User


class RestClient:

    def __init__(self, token: str):
        self.token = token

    def post_message(
            self,
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
            "token": self.token,
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

    def get_channels(self) -> list[Channel]:
        """
        https://api.slack.com/methods/channels.list
        """
        data = {
            "token": self.token,
        }
        params = urllib.parse.urlencode(data)
        res = urllib.request.urlopen("https://slack.com/api/channels.list?{0}".format(params))
        data = json.loads(res.read().decode())
        return [Channel.from_json(obj) for obj in data['channels']]

    def get_users(self) -> list[Channel]:
        """
        https://api.slack.com/methods/users.list
        """
        data = {
            "token": self.token,
        }
        params = urllib.parse.urlencode(data)
        res = urllib.request.urlopen("https://slack.com/api/users.list?{0}".format(params))
        data = json.loads(res.read().decode())
        return [User.from_json(obj) for obj in data['members']]
