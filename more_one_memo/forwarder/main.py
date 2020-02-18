import asyncio

import click

from more_one_memo.forwarder import forwarder
from more_one_memo.forwarder.model import ForwarderConfig


@click.command(context_settings={'auto_envvar_prefix': 'MORE_ONE_MEMO_FORWARDER'})
@click.option('--mongo-uri', help='MongoDB URI. Database name must be included', type=str, required=True, show_envvar=True)
@click.option('--collector-token', help='Slack token of user to receive messages. This user should be able to read messages you want to receive.', type=str,
              required=True, show_envvar=True)
@click.option('--poster-token', help='Slack token of personal user to read messages. This user posts forwarded messages, filters unmuted channels.', type=str,
              required=True, show_envvar=True)
@click.option('--post-channel', help='Slack channel to post forwarded messages', type=str, required=True, show_envvar=True)
@click.option('--debug-channel', help='Slack channel to post debug messages', type=str, required=True, show_envvar=True)
@click.option('--default-username', help='Default username for poster', type=str, default="more-one-memo_forwarder", show_default=True, show_envvar=True)
@click.option('--default-icon-emoji', help='Default icon emoji for poster', type=str, default=":face_with_rolling_eyes:", show_default=True, show_envvar=True)
def main(
    mongo_uri, collector_token, poster_token, post_channel, debug_channel, default_username, default_icon_emoji
):
    forwarder_config = ForwarderConfig(
        mongo_uri, collector_token, poster_token, post_channel, debug_channel, default_username, default_icon_emoji
    )
    asyncio.run(forwarder.run(forwarder_config))
