import argparse
import signal

from google.cloud import datastore

import config
from app.data import put_config, get_config
from app.data.model import DatastoreConfig
from app.forwarder import run, load_user_config
from app.forwarder.model import SlackConfig
from app.model import UserConfig


def main():
    datastore_client = datastore.Client()

    datastore_config = DatastoreConfig(config.DATASTORE_CONFIG_KIND, config.DATASTORE_CONFIG_ID)
    user_config = UserConfig([".*", ], [], [], [])
    put_config(datastore_client, datastore_config, user_config)
    print(get_config(datastore_client, datastore_config))

    slack_config = SlackConfig(
        config.SLACK_COLLECTOR_TOKEN, config.SLACK_PERSONAL_TOKEN,
        config.SLACK_POST_CHANNEL, config.SLACK_DEBUG_CHANNEL,
        config.SLACK_DEFAULT_USERNAME, config.SLACK_DEFAULT_ICON_EMOJI
    )
    run(datastore_config, slack_config)


def reload(_signal, _frame):
    load_user_config()


parser = argparse.ArgumentParser(description='more-one-memo: Slack forwarder.')
parser.add_argument('-d', '--daemon', action='store_true',
                    help='run program as daemon (Reload on SIGHUP, not supported on Windows)')
args = parser.parse_args()

if args.daemon:
    signal.signal(signal.SIGHUP, reload)

main()
