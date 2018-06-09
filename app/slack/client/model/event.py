from typing import NamedTuple, Optional

from .response import ChannelID, UserID


class Message(NamedTuple):
    # https://api.slack.com/events/message

    subtype: Optional[str]
    channel: ChannelID
    user: UserID
    text: Optional[str]

    @staticmethod
    def from_json(json: dict):

        def _get_text(message_json: dict) -> Optional[str]:
            # deleted -> no text
            return message_json.get('text')

        def _get_user(message_json: dict) -> Optional[str]:
            if 'user' in message_json:
                return message_json.get('user')
            else:
                return message_json.get('bot_id')

        if 'message' in json:
            # e.g. thread_broadcast
            message = json['message']
            text = _get_text(message)
            user = _get_user(message)
        else:
            text = _get_text(json)
            user = _get_user(json)
            if user is None:
                if 'comment' in json:
                    # e.g. file_comment
                    user = _get_user(json['comment'])

        # normal message does not have subtype.
        return Message(json.get('subtype'), json['channel'], user, text)
