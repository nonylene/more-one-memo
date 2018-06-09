from typing import NamedTuple, Optional

UserID = str
ChannelID = str


class Channel(NamedTuple):
    """
    https://api.slack.com/types/channel
    """
    id: ChannelID
    name: str
    is_archived: bool

    def get_link(self):
        return f'<#{self.id}|{self.name}>'

    @staticmethod
    def from_json(json: dict):
        return Channel(json['id'], json['name'], json['is_archived'])


class Profile(NamedTuple):
    image_72: str

    @staticmethod
    def from_json(json: dict):
        return Profile(json['image_72'])


class User(NamedTuple):
    """
    https://api.slack.com/types/user
    """
    id: UserID
    name: str
    profile: Profile

    @staticmethod
    def from_json(json: dict):
        return User(json['id'], json['name'], Profile.from_json(json['profile']))

