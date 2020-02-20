from typing import List, Optional
from dataclasses import dataclass

UserID = str
BotID = str
ChannelID = str


@dataclass
class Channel:
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


@dataclass
class User:
    """
    https://api.slack.com/types/user
    """

    @dataclass
    class Profile:
        image_72: Optional[str]
        image_192: Optional[str]

        def get_image(self) -> Optional[str]:
            if self.image_192 is not None:
                return self.image_192

            if self.image_72 is not None:
                return self.image_72

            return None

        @staticmethod
        def from_json(json: dict):
            return User.Profile(json['image_72'], json['image_192'])

    id: UserID
    name: str
    profile: Profile

    @staticmethod
    def from_json(json: dict):
        return User(json['id'], json['name'], User.Profile.from_json(json['profile']))


@dataclass
class RtmStart:
    # https://api.slack.com/methods/rtm.start

    @dataclass
    class Self:
        @dataclass
        class Prefs:
            muted_channels: List[str]

            @staticmethod
            def from_json(json: dict):
                return RtmStart.Self.Prefs(json['muted_channels'])

        prefs: Prefs

        @staticmethod
        def from_json(json: dict):
            return RtmStart.Self(
                RtmStart.Self.Prefs.from_json(json['prefs'])
            )

    url: str
    self_: Self
    users: List[User]
    channels: List[Channel]

    @staticmethod
    def from_json(json: dict):
        return RtmStart(
            json['url'],
            RtmStart.Self.from_json(json['self']),
            [User.from_json(user) for user in json['users']],
            [Channel.from_json(channel) for channel in json['channels']],
        )


@dataclass
class RtmConnect:
    # https://api.slack.com/methods/rtm.connect

    url: str

    @staticmethod
    def from_json(json: dict):
        return RtmConnect(
            json['url'],
        )
