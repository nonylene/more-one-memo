from typing import Optional
from dataclasses import dataclass

from more_one_memo.slack.model.response import ChannelID, UserID, BotID


@dataclass
class Message:
    # https://api.slack.com/events/message

    @dataclass
    # Shown in message_changed, thread_broadcast, ...
    class Message:
        type_: str
        subtype: Optional[str]
        user: Optional[UserID]
        bot_id: Optional[BotID]
        text: Optional[str]

        @staticmethod
        def from_json(json: dict):
            return Message.Message(
                json['type'], json.get('subtype'), json.get('user'), json.get('bot_id'), json.get('text')
            )

    subtype: Optional[str]
    channel: ChannelID
    user: Optional[UserID]
    bot_id: Optional[BotID]
    text: Optional[str]
    message: Optional[Message]
    previous_message: Optional[Message]

    def get_text(self) -> Optional[str]:
        if self.text is not None:
            return self.text

        if self.message is not None:
            return self.message.text

        return None

    def get_user(self) -> Optional[UserID]:
        if self.user is not None:
            return self.user

        if self.message is not None:
            return self.message.user

        return None

    def get_bot_id(self) -> Optional[BotID]:
        if self.bot_id is not None:
            return self.bot_id

        if self.message is not None:
            return self.message.bot_id

        return None

    @staticmethod
    def from_json(json: dict):
        # Deleted -> no text
        text = json.get('text')
        user = json.get('user')
        if user is None:
            if 'comment' in json:
                # e.g. file_comment
                user = json['comment'].get('user')
        bot_id = json.get('bot_id')
        if bot_id is None:
            if 'comment' in json:
                # e.g. file_comment
                bot_id = json['comment'].get('bot_id')

        message: Optional[Message.Message] = None
        previous_message: Optional[Message.Message] = None
        if 'message' in json:
            message = Message.Message.from_json(json['message'])
        if 'previous_message' in json:
            previous_message = Message.Message.from_json(json['previous_message'])

        # normal message does not have subtype.
        return Message(json.get('subtype'), json['channel'], user, bot_id, text, message, previous_message)
