from google.cloud import datastore

from ..model import UserConfig


def _update_entity(entity: datastore.Entity, config: UserConfig):
    entity['id'] = config.id


def put_config(client: datastore.Client, kind: str, config: UserConfig):
    config_key = client.key(kind, config.id)
    config_entity = datastore.Entity(key=config_key)
    _update_entity(config_entity, config)
    client.put(config_entity)


def get_config(client: datastore.Client, kind: str, id: str) -> UserConfig:
    config_key = client.key(kind, id)
    entity = client.get(config_key)
    return UserConfig.from_entity(entity)
