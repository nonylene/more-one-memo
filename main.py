import config
from app.slack import run_client
from app.slack.model import SlackConfig

# DATASTORE_CLIENT = datastore.Client()
#
# user_config = UserConfig("aa")
# put_config(DATASTORE_CLIENT, config.DATASTORE_CONFIG_KIND, user_config)
# print(get_config(DATASTORE_CLIENT, config.DATASTORE_CONFIG_KIND, "aa"))


slack_config = SlackConfig(
    config.SLACK_COLLECTOR_TOKEN, config.SLACK_PERSONAL_TOKEN,
    config.SLACK_POST_CHANNEL, config.SLACK_DEBUG_CHANNEL,
    config.SLACK_DEFAULT_USERNAME, config.SLACK_DEFAULT_ICON_EMOJI
)

run_client(slack_config)
