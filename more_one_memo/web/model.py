from dataclasses import dataclass
from typing import Dict

from more_one_memo.slack import model as slack_model


@dataclass
class WebConfig:
    mongo_uri: str
    slack_token: str
    host: str
    port: int


@dataclass
class Channel:
    id: str
    name: str

    @staticmethod
    def from_api(api_channel: slack_model.Channel):
        return Channel(api_channel.id, api_channel.name)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
        }


@dataclass
class User:
    id: str
    name: str

    @staticmethod
    def from_api(api_user: slack_model.User):
        return User(api_user.id, api_user.name)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
        }
