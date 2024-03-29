import click
from more_one_memo.web import web
from more_one_memo.web.model import WebConfig


@click.command(context_settings={'auto_envvar_prefix': 'MORE_ONE_MEMO_WEB'})
@click.option('--mongo-uri', help='MongoDB URI. Database name must be included', type=str, required=True, show_envvar=True)
@click.option('--slack-token', help='Slack token to get channel and user information', type=str, required=True, show_envvar=True)
@click.option('--host', help='Bind host address', type=str, default="127.0.0.1", show_default=True, show_envvar=True)
@click.option('--port', help='Bind port', type=int, default=8080, show_default=True, show_envvar=True)
def main(mongo_uri, slack_token, host, port):
    web_config = WebConfig(mongo_uri, slack_token, host, port)
    web.run(web_config)
