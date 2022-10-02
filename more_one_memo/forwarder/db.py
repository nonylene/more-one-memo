from more_one_memo import data
from more_one_memo.forwarder.instance import GLOBAL_INSTANCE
from more_one_memo.model import UserConfig
from pymongo import MongoClient

client: MongoClient = None


async def get_user_config() -> UserConfig:
    return await data.get_user_config(GLOBAL_INSTANCE.mongo_client)


async def set_user_config(user_config: UserConfig):
    await data.upsert_user_config(GLOBAL_INSTANCE.mongo_client, user_config)


async def init_db():
    if await data.get_user_config_optional(GLOBAL_INSTANCE.mongo_client) is None:
        # Init user config
        await set_user_config(UserConfig.init())
