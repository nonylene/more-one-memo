import motor.motor_asyncio
from aiohttp import web
from more_one_memo import data
from more_one_memo.model import UserConfig
from more_one_memo.web.model import WebConfig

APP_CLIENT_KEY = 'mongo'


async def get_user_config(app: web.Application) -> UserConfig:
    return await data.get_user_config(app[APP_CLIENT_KEY])


async def upsert_user_config(app: web.Application, user_config: UserConfig):
    await data.upsert_user_config(app[APP_CLIENT_KEY], user_config)


async def init_db(app: web.Application):
    web_config: WebConfig = app['config']
    client = motor.motor_asyncio.AsyncIOMotorClient(web_config.mongo_uri)
    app[APP_CLIENT_KEY] = client
    if await data.get_user_config_optional(client) is None:
        # Init user config
        await upsert_user_config(app, UserConfig.init())


async def close_db(app: web.Application):
    app[APP_CLIENT_KEY].close()
