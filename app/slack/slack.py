from .client import WebSocketClient, RestClient
from .model import SlackConfig


def logger(slack_config: SlackConfig, rest_client: RestClient, text: str):
    print(text)
    rest_client.post_message(
        text,
        slack_config.debug_channel,
        slack_config.default_username,
        slack_config.default_icon_emoji
    )


def run_client(slack_config: SlackConfig):
    rest_client = RestClient(slack_config.personal_token)
    client = WebSocketClient(slack_config, lambda text: logger(slack_config, rest_client, text))
    client.run()
