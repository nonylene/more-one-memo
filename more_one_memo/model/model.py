"""
Common models.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class UserConfig:
    channel_regexps_member: List[str]
    channel_regexps_nomember: List[str]
    ignore_channels: List[str]
    ignore_users: List[str]

    @staticmethod
    def init():
        # Ignore Slackbot by default
        return UserConfig([".*"], [".*"], [], ["USLACKBOT"])

    @staticmethod
    def from_dict(value: Dict):
        def _check_items(items: Any, name: str):
            items_type = type(items)
            if items_type != list:
                raise TypeError(
                    f"{name} type should be list or empty but got {items_type}."
                )

            for item in items:
                item_type = type(item)
                if item_type != str:
                    raise TypeError(
                        f"Item in {name} type should be str but got {item_type}."
                    )

        def _get_or_empty(dic: Dict, key: str):
            item = dic[key] if key in dic else []
            _check_items(item, key)
            return item

        return UserConfig(
            _get_or_empty(value, "channel_regexps_member"),
            _get_or_empty(value, "channel_regexps_nomember"),
            _get_or_empty(value, "ignore_channels"),
            _get_or_empty(value, "ignore_users"),
        )

    def to_dict(self) -> Dict:
        return {
            "channel_regexps_member": self.channel_regexps_member,
            "channel_regexps_nomember": self.channel_regexps_nomember,
            "ignore_channels": self.ignore_channels,
            "ignore_users": self.ignore_users,
        }
