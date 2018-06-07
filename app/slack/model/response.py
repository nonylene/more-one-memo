from typing import NamedTuple


class Channel(NamedTuple):
    """
    https://api.slack.com/types/channel
    """
    id: str
    name: str

    def get_link(self):
        return '<#{0}|{1}>'.format(self.id, self.name)

    @staticmethod
    def from_json(json: dict):
        return Channel(json['id'], json['name'])


class Profile(NamedTuple):
    image_72: str

    @staticmethod
    def from_json(json: dict):
        return Profile(json['image_72'])


class User(NamedTuple):
    """
    https://api.slack.com/types/user
    """
    id: str
    name: str
    profile: Profile

    @staticmethod
    def from_json(json: dict):
        return User(json['id'], json['name'], Profile.from_json(json['profile']))
