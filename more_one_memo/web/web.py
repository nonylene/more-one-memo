# from flask import Flask, request, jsonify
from aiohttp import web

from more_one_memo.web.model import WebConfig
from more_one_memo.web.db import get_user_config, upsert_user_config, init_db, close_db
from more_one_memo.model import UserConfig

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


app.add_routes(routes)
app.on_startup.append(init_db)
app.on_shutdown.append(close_db)


def run(web_config: WebConfig):
    app['config'] = web_config
    web.run_app(app, host=web_config.host, port=web_config.port)
