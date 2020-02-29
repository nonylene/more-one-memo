# from flask import Flask, request, jsonify
import asyncio
from typing import List

from aiohttp import web

from more_one_memo.slack import RestClient
import more_one_memo.slack.model as slack_model
from more_one_memo.web.model import WebConfig, User, Channel
from more_one_memo.web.db import get_user_config, upsert_user_config, init_db, close_db
from more_one_memo.model import UserConfig

SLACK_CLIENT_KEY = 'slack_client'


async def init_slack(app: web.Application):
    web_config: WebConfig = app['config']
    app[SLACK_CLIENT_KEY] = RestClient(web_config.slack_token)


def get_slack_client(app: web.Application) -> RestClient:
    return app[SLACK_CLIENT_KEY]


routes = web.RouteTableDef()
app = web.Application()


@routes.get('/api/config')
async def get_config(request: web.Request):
    config = await get_user_config(app)
    return web.json_response(config.to_dict())


@routes.post('/api/config')
async def post_config(request: web.Request):
    posted_json = await request.json()
    await upsert_user_config(app, UserConfig.from_dict(posted_json))
    return web.json_response((await get_user_config(app)).to_dict())


@routes.get('/api/slack/channels')
async def slack_channels(request: web.Request):
    api_channels: List[slack_model.Channel] = []
    next_cursor = None
    while True:
        conversations = await get_slack_client(app).get_public_channels(cursor=next_cursor)
        api_channels.extend(conversations.channels)
        if not conversations.response_metadata.next_cursor:
            break
        await asyncio.sleep(0.5)
        next_cursor = conversations.response_metadata.next_cursor
    # Return active channels only
    channels = map(Channel.from_api, filter(lambda c: not c.is_archived, api_channels))
    return web.json_response([c.to_dict() for c in channels])


@routes.get('/api/slack/users')
async def slack_users(request: web.Request):
    api_users: List[slack_model.User] = []
    next_cursor = None
    while True:
        slack_users = await get_slack_client(app).get_users(cursor=next_cursor)
        api_users.extend(slack_users.members)
        if not slack_users.response_metadata.next_cursor:
            break
        await asyncio.sleep(0.5)
        next_cursor = api_users.response_metadata.next_cursor
    users = map(User.from_api, api_users)
    return web.json_response([u.to_dict() for u in users])


app.add_routes(routes)
app.on_startup.append(init_db)
app.on_startup.append(init_slack)
app.on_shutdown.append(close_db)


def run(web_config: WebConfig):
    app['config'] = web_config
    web.run_app(app, host=web_config.host, port=web_config.port)
