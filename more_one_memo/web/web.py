from flask import Flask, request, jsonify

from more_one_memo.web.model import WebConfig
from more_one_memo.web.db import get_user_config, upsert_user_config, init_db
from more_one_memo.model import UserConfig

app = Flask(__name__)


@app.route('/config', methods=['GET'])
def get_config():
    config = get_user_config()
    return jsonify(config.to_dict())


@app.route('/config', methods=['POST'])
def post_config():
    posted_json = request.json
    upsert_user_config(UserConfig.from_dict(posted_json))
    return jsonify(get_user_config().to_dict())


def run(web_config: WebConfig):
    init_db(web_config)
    app.run(web_config.host, web_config.port)
