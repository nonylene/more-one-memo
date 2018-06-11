from google.cloud import datastore

import config
from app.data import put_config, get_config
from app.data.model import DatastoreConfig
from app.model import UserConfig
from app.slack import run_client
from app.slack.model import SlackConfig

DATASTORE_CLIENT = datastore.Client()

datastore_config = DatastoreConfig(config.DATASTORE_CONFIG_KIND, config.DATASTORE_CONFIG_ID)
user_config = UserConfig([".*", ], [], [], [])
put_config(DATASTORE_CLIENT, datastore_config, user_config)
print(get_config(DATASTORE_CLIENT, datastore_config))

slack_config = SlackConfig(
    config.SLACK_COLLECTOR_TOKEN, config.SLACK_PERSONAL_TOKEN,
    config.SLACK_POST_CHANNEL, config.SLACK_DEBUG_CHANNEL,
    config.SLACK_DEFAULT_USERNAME, config.SLACK_DEFAULT_ICON_EMOJI
)

run_client(datastore_config, slack_config)
