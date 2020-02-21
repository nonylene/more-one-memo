# from flask import Flask, request, jsonify
from aiohttp import web

from more_one_memo.slack import RestClient
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


@routes.get('/config')
async def get_config(request: web.Request):
    config = await get_user_config(app)
    return web.json_response(config.to_dict())


@routes.post('/config')
async def post_config(request: web.Request):
    posted_json = await request.json()
    await upsert_user_config(app, UserConfig.from_dict(posted_json))
    return web.json_response((await get_user_config(app)).to_dict())


@routes.get('/slack/channels')
async def slack_channels(request: web.Request):
    channels = map(Channel.from_api, await get_slack_client(app).get_channels())
    return web.json_response([c.to_dict() for c in channels])


@routes.get('/slack/users')
async def slack_users(request: web.Request):
    users = map(User.from_api, await get_slack_client(app).get_users())
    return web.json_response([u.to_dict() for u in users])


app.add_routes(routes)
app.on_startup.append(init_db)
app.on_startup.append(init_slack)
app.on_shutdown.append(close_db)


def run(web_config: WebConfig):
    app['config'] = web_config
    web.run_app(app, host=web_config.host, port=web_config.port)
