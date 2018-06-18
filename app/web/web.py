import functools
from typing import Callable

from flask import Flask, request, abort, jsonify
from google.cloud import datastore

from . import util
from .model import WebConfig
from .. import data
from ..data.model import DatastoreConfig
from ..model import UserConfig

app = Flask(__name__)

_API_HEADER_KEY = 'x-api-key'

_DATASTORE_CLIENT = datastore.Client()


def _with_api_key(func: Callable) -> Callable:
    """
    :return: Function with api key filter.
    """

    @functools.wraps(func)
    def _filtered_func(*args, **kwargs):
        if request.headers.get(_API_HEADER_KEY) == util.get_web_config(app).api_key:
            return func(*args, **kwargs)
        else:
            return abort(401)

    return _filtered_func


@app.route('/config', methods=['GET'])
@_with_api_key
def get_config():
    config = data.get_config(_DATASTORE_CLIENT, util.get_datastore_config(app))
    return jsonify(config.to_dict())


@app.route('/config', methods=['POST'])
@_with_api_key
def post_config():
    posted_json = request.json
    config = UserConfig.from_json(posted_json)
    data.put_config(_DATASTORE_CLIENT, util.get_datastore_config(app), config)
    return jsonify(config.to_dict())


def run(web_config: WebConfig, datastore_config: DatastoreConfig):
    util.put_web_config(app, web_config)
    util.put_datastore_config(app, datastore_config)
    app.run(web_config.host, web_config.port)
