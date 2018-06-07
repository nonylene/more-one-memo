import json
import urllib.parse
import urllib.request
from typing import List

from ..model import Channel, User


class RestClient:

    def __init__(self, token: str):
        self.token = token

    def post_message(self, text: str, channel: str, username: str, icon_emoji: str) -> None:
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

    def get_channels(self) -> List[Channel]:
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

    def get_users(self) -> List[Channel]:
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
