from typing import NamedTuple, List

UserID = str
BotID = str
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


class User(NamedTuple):
    """
    https://api.slack.com/types/user
    """

    class Profile(NamedTuple):
        image_72: str

        @staticmethod
        def from_json(json: dict):
            return User.Profile(json['image_72'])

    id: UserID
    name: str
    profile: Profile

    @staticmethod
    def from_json(json: dict):
        return User(json['id'], json['name'], User.Profile.from_json(json['profile']))


class Bot(NamedTuple):
    class Icons(NamedTuple):
        image_72: str

        @staticmethod
        def from_json(json: dict):
            return Bot.Icons(json['image_72'])

    id: UserID
    name: str
    icons: Icons

    @staticmethod
    def from_json(json: dict):
        return Bot(json['id'], json['name'], Bot.Icons.from_json(json['icons']))


class RtmStart(NamedTuple):
    # https://api.slack.com/methods/rtm.start

    class Self(NamedTuple):
        class Prefs(NamedTuple):
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
