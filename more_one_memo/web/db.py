from pymongo import MongoClient

from more_one_memo import data
from more_one_memo.model import UserConfig

from more_one_memo.web.model import WebConfig


client: MongoClient = None


def get_user_config() -> UserConfig:
    return data.get_user_config(client)


def upsert_user_config(user_config: UserConfig):
    data.upsert_user_config(client, user_config)


def init_db(web_config: WebConfig):
    global client
    client = MongoClient(web_config.mongo_uri)
    if data.get_user_config_optional(client) is None:
        # Init user config
        upsert_user_config(UserConfig.init())
