from dataclasses import dataclass
from typing import List, Optional

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
    is_member: bool

    @staticmethod
    def from_json(json: dict):
        return Channel(json['id'], json['name'], json['is_archived'], json['is_member'])


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
class Conversations:
    # https://api.slack.com/methods/conversations.list

    @dataclass
    class ResponseMetadata:
        next_cursor: Optional[str]

        @staticmethod
        def from_json(json: dict):
            return Conversations.ResponseMetadata(json.get('next_cursor'))

    channels: List[Channel]  # Regard Conversation as Channel
    response_metadata: ResponseMetadata

    @staticmethod
    def from_json(json: dict):
        return Conversations(
            [Channel.from_json(obj) for obj in json['channels']],
            Conversations.ResponseMetadata.from_json(json['response_metadata'])
        )


@dataclass
class Users:
    # https://api.slack.com/methods/users.list

    @dataclass
    class ResponseMetadata:
        next_cursor: Optional[str]

        @staticmethod
        def from_json(json: dict):
            return Users.ResponseMetadata(json.get('next_cursor'))

    members: List[User]
    response_metadata: ResponseMetadata

    @staticmethod
    def from_json(json: dict):
        return Users(
            [User.from_json(obj) for obj in json['members']],
            Users.ResponseMetadata.from_json(json['response_metadata'])
        )


@dataclass
class RtmConnect:
    # https://api.slack.com/methods/rtm.connect

    @dataclass
    class Self:

        id: UserID

        @staticmethod
        def from_json(json: dict):
            return RtmConnect.Self(
                json['id'],
            )

    @dataclass
    class Team:
        domain: str

        @staticmethod
        def from_json(json: dict):
            return RtmConnect.Team(json['domain'])

    url: str
    self_: Self
    team: Team

    @staticmethod
    def from_json(json: dict):
        return RtmConnect(
            json['url'],
            RtmConnect.Self.from_json(json['self']),
            RtmConnect.Team.from_json(json['team']),
        )


@dataclass
class UserPrefs:
    # https://github.com/slack-go/slack/blob/master/info.go

    @dataclass
    class Prefs:
        # comma-separated channels
        muted_channels: str

        def get_muted_channels(self) -> list[str]:
            return self.muted_channels.split(',')

        @staticmethod
        def from_json(json: dict):
            return UserPrefs.Prefs(json['muted_channels'])

    prefs: Prefs

    @staticmethod
    def from_json(json: dict):
        return UserPrefs(
            UserPrefs.Prefs.from_json(json['prefs']),
        )
