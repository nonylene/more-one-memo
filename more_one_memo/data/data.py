from pymongo import MongoClient
from typing import Optional

from more_one_memo.model import UserConfig

_USER_CONFIG_COLLECTION = 'user-config'


def upsert_user_config(client: MongoClient, user_config: UserConfig) -> str:
    collection = client.get_default_database()[_USER_CONFIG_COLLECTION]
    result = collection.replace_one(
        {}, user_config.to_dict(), upsert=True
    )
    return result.upserted_id


def get_user_config_optional(client: MongoClient) -> Optional[UserConfig]:
    collection = client.get_default_database()[_USER_CONFIG_COLLECTION]
    config = collection.find_one(None)
    if config is None:
        return None

    return UserConfig.from_dict(config)


def get_user_config(client: MongoClient) -> UserConfig:
    config = get_user_config_optional(client)
    if config is None:
        raise RuntimeError("No document for user config found in {USER_CONFIG_COLLECTION}")
    return config
