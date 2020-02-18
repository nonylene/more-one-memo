import httpx
from typing import List, Optional

from more_one_memo.slack.model import Channel, User, RtmStart, RtmConnect


class RestClient:

    def __init__(self, token: str):
        self.client = httpx.AsyncClient(
            headers={'Authorization': f'Bearer {token}'}
        )

    async def post_message(
            self, text: str, channel: str, username: str,
            icon_emoji: Optional[str], icon_url: Optional[str]
    ) -> None:
        data = {
            'channel': channel,
            'text': text,
            'username': username
        }
        if icon_emoji:
            data['icon_emoji'] = icon_emoji
        if icon_url:
            data['icon_url'] = icon_url

        await self.client.get('https://slack.com/api/chat.postMessage', params=data)

    async def get_channels(self) -> List[Channel]:
        # https://api.slack.com/methods/channels.list
        r = await self.client.get('https://slack.com/api/channels.list')
        data = r.json()
        return [Channel.from_json(obj) for obj in data['channels']]

    async def get_users(self) -> List[User]:
        # https://api.slack.com/methods/users.list
        r = await self.client.get('https://slack.com/api/users.list')
        data = r.json()
        return [User.from_json(obj) for obj in data['members']]

    async def rtm_start(self):
        # https://api.slack.com/methods/rtm.start
        data = {
            'no_latest': 1,
        }
        r = await self.client.get('https://slack.com/api/rtm.start', params=data)
        data = r.json()
        return RtmStart.from_json(data)

    async def rtm_connect(self):
        # https://api.slack.com/methods/rtm.connect
        r = await self.client.get('https://slack.com/api/rtm.connect')
        data = r.json()
        return RtmConnect.from_json(data)
