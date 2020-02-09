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

        @staticmethod
        def from_json(json: dict):
            return User.Profile(json['image_72'])

    id: UserID
    name: str
    profile: Profile

    @staticmethod
    def from_json(json: dict):
        return User(json['id'], json['name'], User.Profile.from_json(json['profile']))


@dataclass
class Bot:
    @dataclass
    class Icons:
        image_64: Optional[str]  # Some bot users does not have image_72
        image_72: str

        @staticmethod
        def from_json(json: dict):
            return Bot.Icons(json.get('image_64'), json.get('image_72'))

    id: UserID
    name: str
    icons: Icons

    @staticmethod
    def from_json(json: dict):
        return Bot(json['id'], json['name'], Bot.Icons.from_json(json['icons']))


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
    bots: List[Bot]

    @staticmethod
    def from_json(json: dict):
        return RtmStart(
            json['url'],
            RtmStart.Self.from_json(json['self']),
            [User.from_json(user) for user in json['users']],
            [Channel.from_json(channel) for channel in json['channels']],
            [Bot.from_json(bot) for bot in json['bots']],
        )
