from pymongo import MongoClient

from more_one_memo.forwarder.instance import GLOBAL_INSTANCE
from more_one_memo.model import UserConfig
from more_one_memo import data


client: MongoClient = None


def get_user_config() -> UserConfig:
    return data.get_user_config(GLOBAL_INSTANCE.mongo_client)


def set_user_config(user_config: UserConfig):
    data.upsert_user_config(GLOBAL_INSTANCE.mongo_client, user_config)


def init_db():
    if data.get_user_config_optional(GLOBAL_INSTANCE.mongo_client) is None:
        # Init user config
        set_user_config(UserConfig.init())
