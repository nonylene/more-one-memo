from typing import List
import asyncio

from more_one_memo.slack.rest import RestClient
from more_one_memo.slack.model import User, Channel


async def get_all_users(client: RestClient) -> List[User]:
    users: List[User] = []
    next_cursor = None
    while True:
        slack_users = await client.get_users(cursor=next_cursor)
        users.extend(slack_users.members)
        if not slack_users.response_metadata.next_cursor:
            break
        await asyncio.sleep(0.5)
        next_cursor = users.response_metadata.next_cursor
    return users


async def get_all_channels(client: RestClient) -> List[Channel]:
    channels: List[Channel] = []
    next_cursor = None
    while True:
        conversations = await client.get_public_channels(cursor=next_cursor)
        channels.extend(conversations.channels)
        if not conversations.response_metadata.next_cursor:
            break
        await asyncio.sleep(0.5)
        next_cursor = conversations.response_metadata.next_cursor
    return channels
