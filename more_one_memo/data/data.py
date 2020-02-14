from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from more_one_memo.model import UserConfig

_USER_CONFIG_COLLECTION = 'user-config'


async def upsert_user_config(client: AsyncIOMotorClient, user_config: UserConfig) -> str:
    collection: AsyncIOMotorCollection = client.get_default_database()[_USER_CONFIG_COLLECTION]
    result = await collection.replace_one(
        {}, user_config.to_dict(), upsert=True
    )
    return result.upserted_id


async def get_user_config_optional(client: AsyncIOMotorClient) -> Optional[UserConfig]:
    collection = client.get_default_database()[_USER_CONFIG_COLLECTION]
    config = await collection.find_one(None)
    if config is None:
        return None

    return UserConfig.from_dict(config)


async def get_user_config(client: AsyncIOMotorClient) -> UserConfig:
    config = await get_user_config_optional(client)
    if config is None:
        raise RuntimeError("No document for user config found in {USER_CONFIG_COLLECTION}")
    return config
