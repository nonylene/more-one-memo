from typing import Optional
from dataclasses import dataclass

from more_one_memo.slack.model.response import ChannelID, UserID, BotID


@dataclass
class Message:
    # https://api.slack.com/events/message

    subtype: Optional[str]
    channel: ChannelID
    user: UserID
    bot: BotID
    text: Optional[str]

    @staticmethod
    def from_json(json: dict):

        def _get_text(message_json: dict) -> Optional[str]:
            # deleted -> no text
            return message_json.get('text')

        def _get_user(message_json: dict) -> Optional[UserID]:
            return message_json.get('user')

        def _get_bot(message_json: dict) -> Optional[BotID]:
            return message_json.get('bot_id')

        if 'message' in json:
            # e.g. thread_broadcast
            message = json['message']
            text = _get_text(message)
            user = _get_user(message)
            bot = _get_bot(message)
        else:
            text = _get_text(json)
            user = _get_user(json)
            bot = _get_bot(json)
            if user is None and bot is None:
                if 'comment' in json:
                    # e.g. file_comment
                    comment = json['comment']
                    user = _get_user(comment)
                    bot = _get_bot(comment)

        # normal message does not have subtype.
        return Message(json.get('subtype'), json['channel'], user, bot, text)
