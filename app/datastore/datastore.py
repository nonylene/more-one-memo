from google.cloud import datastore

from ..model import UserConfig

CLIENT = datastore.Client()


def _update_entity(entity: datastore.Entity, config: UserConfig):
    entity['id'] = config.id


def put_config(kind: str, config: UserConfig):
    config_key = CLIENT.key(kind, config.id)
    config_entity = datastore.Entity(key=config_key)
    _update_entity(config_entity, config)
    CLIENT.put(config_entity)


def get_config(kind: str, id: str) -> UserConfig:
    config_key = CLIENT.key(kind, id)
    entity = CLIENT.get(config_key)
    return UserConfig.from_entity(entity)
