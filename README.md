# more-one-memo

Post Slack messages from **multiple** channels into a **single** channel.

Unlike "All unreads" feature in Slack, messages are sorted by their posted time.

This app also have API and web interface to configure.

## more-one-memo\_web, more-one-memo\_forwarder

### Requirements

- Docker

or

- Python 3.10 ~
  - poetry
- MongoDB

### Setup

```bash
$ docker compose build
```

or

```bash
$ poetry install
```

### Forwarder

```
$ poetry run more-one-memo_forwarder --help
Usage: more-one-memo_forwarder [OPTIONS]

Options:
  --mongo-uri TEXT           MongoDB URI. Database name must be included  [env
                             var: MORE_ONE_MEMO_FORWARDER_MONGO_URI; required]
  --collector-token TEXT     Slack token of user to receive messages. This
                             user should be able to read messages you want to
                             receive.  [env var:
                             MORE_ONE_MEMO_FORWARDER_COLLECTOR_TOKEN;
                             required]
  --poster-token TEXT        Slack token of personal user to read messages.
                             This user posts forwarded messages, filters
                             unmuted channels.  [env var:
                             MORE_ONE_MEMO_FORWARDER_POSTER_TOKEN; required]
  --post-channel TEXT        Slack channel to post forwarded messages  [env
                             var: MORE_ONE_MEMO_FORWARDER_POST_CHANNEL;
                             required]
  --debug-channel TEXT       Slack channel to post debug messages  [env var:
                             MORE_ONE_MEMO_FORWARDER_DEBUG_CHANNEL; required]
  --default-username TEXT    Default username for poster  [env var:
                             MORE_ONE_MEMO_FORWARDER_DEFAULT_USERNAME;
                             default: more-one-memo_forwarder]
  --default-icon-emoji TEXT  Default icon emoji for poster  [env var:
                             MORE_ONE_MEMO_FORWARDER_DEFAULT_ICON_EMOJI;
                             default: :face_with_rolling_eyes:]
  --help                     Show this message and exit.
```

### Web

Slack token needs `channels:read` and `users:read` permission scopes.

**Caution**: This app has no authentication, so you should run this under authentication proxy (e.g. [oauth2_proxy](https://github.com/pusher/oauth2_proxy)) or firewall.

```
$ poetry run more-one-memo_web --help
Usage: more-one-memo_web [OPTIONS]

Options:
  --mongo-uri TEXT  MongoDB URI. Database name must be included  [env var:
                    MORE_ONE_MEMO_WEB_MONGO_URI; required]
  --slack-token TEXT  Slack token to get channel and user information  [env
                    var: MORE_ONE_MEMO_WEB_SLACK_TOKEN; required]
  --address TEXT    Bind address  [env var: MORE_ONE_MEMO_WEB_ADDRESS;
                    default: 127.0.0.1]
  --port INTEGER    Bind port  [env var: MORE_ONE_MEMO_WEB_PORT; default:
                    5000]
  --help            Show this message and exit.
```

### Development

See [docker-compose.yaml](./docker-compose.yaml)

```console
# Web / console development
$ docker compose up
```

```console
# Forwarder development
$ docker compose -f ./docker-compose.forwarder.yml up
```

## more-one-memo\_console

React app to configure forwarder. more-one-memo_web should be deployed under the same domain.

### Requirements

- Docker

or

- nodejs 12 ~

### Setup

```bash
$ docker compose build
```

or

```bash
$ cd console
$ npm install
```

### Run

```bash
$ docker compose up
```

or

See [console/README.md](./console/README.md)

## License

See [LICENSE](./LICENSE) for more-one-memo and [DOCKER_NOTICE](https://github.com/nonylene/more-one-memo/blob/main/DOCKER_NOTICE) for Docker image notices.
