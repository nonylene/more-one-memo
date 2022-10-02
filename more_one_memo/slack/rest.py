from typing import Any, Optional

import httpx
from more_one_memo.slack.model import (Conversations, RtmConnect, RtmStart,
                                       Users)


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

    async def get_public_channels(self, exclude_archived=True, cursor: Optional[str] = None) -> Conversations:
        # https://api.slack.com/methods/channels.list
        data = {
            'limit': 1000,
            'exclude_archived': exclude_archived,
        }
        if cursor is not None:
            data['cursor'] = cursor
        r = await self.client.get('https://slack.com/api/conversations.list', params=data)
        data = r.json()
        return Conversations.from_json(data)

    async def get_users(self, cursor: Optional[str] = None) -> Users:
        # https://api.slack.com/methods/users.list
        data: dict[str, Any] = {'limit': 1000}
        if cursor is not None:
            data['cursor'] = cursor
        r = await self.client.get('https://slack.com/api/users.list', params=data)
        data = r.json()
        return Users.from_json(data)

    async def rtm_start(self) -> RtmStart:
        # https://api.slack.com/methods/rtm.start
        data = {
            'no_latest': 1,
        }
        r = await self.client.get('https://slack.com/api/rtm.start', params=data)
        data = r.json()
        return RtmStart.from_json(data)

    async def rtm_connect(self) -> RtmConnect:
        # https://api.slack.com/methods/rtm.connect
        r = await self.client.get('https://slack.com/api/rtm.connect')
        data = r.json()
        return RtmConnect.from_json(data)
