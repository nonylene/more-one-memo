from google.cloud import datastore

from .model import DatastoreConfig
from ..model import UserConfig


def put_config(client: datastore.Client, datastore_config: DatastoreConfig, user_config: UserConfig):
    config_key = client.key(datastore_config.kind, datastore_config.id)
    config_entity = datastore.Entity(key=config_key)
    user_config.update_entity(config_entity)
    client.put(config_entity)


def get_config(client: datastore.Client, datastore_config: DatastoreConfig) -> UserConfig:
    config_key = client.key(datastore_config.kind, datastore_config.id)
    entity = client.get(config_key)
    return UserConfig.from_entity(entity)
