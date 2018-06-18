from flask import Flask

from .model import WebConfig
from ..data.model import DatastoreConfig

_WEB_CONFIG_KEY = 'web_config'
_DATASTORE_CONFIG_KEY = 'datastore_config'


def get_web_config(app: Flask) -> WebConfig:
    return app.config[_WEB_CONFIG_KEY]


def put_web_config(app: Flask, web_config: WebConfig):
    app.config[_WEB_CONFIG_KEY] = web_config


def get_datastore_config(app: Flask) -> DatastoreConfig:
    return app.config[_DATASTORE_CONFIG_KEY]


def put_datastore_config(app: Flask, datastore_config: DatastoreConfig):
    app.config[_DATASTORE_CONFIG_KEY] = datastore_config
