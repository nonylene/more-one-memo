import json
import urllib.parse
import urllib.request
from typing import List, Optional

from more_one_memo.slack.model import Channel, User, RtmStart


class RestClient:

    def __init__(self, token: str):
        self.token = token

    def post_message(
            self, text: str, channel: str, username: str,
            icon_emoji: Optional[str], icon_url: Optional[str]
    ) -> None:
        data = {
            'token': self.token,
            'channel': channel,
            'text': text,
            'username': username
        }
        if icon_emoji:
            data['icon_emoji'] = icon_emoji
        if icon_url:
            data['icon_url'] = icon_url

        post_data = urllib.parse.urlencode(data).encode()
        urllib.request.urlopen(
            'https://slack.com/api/chat.postMessage',
            data=post_data
        )

    def get_channels(self) -> List[Channel]:
        # https://api.slack.com/methods/channels.list
        data = {
            "token": self.token,
        }
        params = urllib.parse.urlencode(data)
        res = urllib.request.urlopen("https://slack.com/api/channels.list?{0}".format(params))
        data = json.loads(res.read().decode())
        return [Channel.from_json(obj) for obj in data['channels']]

    def get_users(self) -> List[User]:
        # https://api.slack.com/methods/users.list
        data = {
            "token": self.token,
        }
        params = urllib.parse.urlencode(data)
        res = urllib.request.urlopen("https://slack.com/api/users.list?{0}".format(params))
        data = json.loads(res.read().decode())
        return [User.from_json(obj) for obj in data['members']]

    def rtm_start(self):
        # https://api.slack.com/methods/rtm.start
        data = {
            'token': self.token,
            'no_latest': 1,
            'no_unreads': 1,
        }
        params = urllib.parse.urlencode(data)
        res = urllib.request.urlopen('https://slack.com/api/rtm.start?{0}'.format(params))
        data = json.loads(res.read().decode())
        return RtmStart.from_json(data)
