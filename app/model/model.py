"""
Common models.
"""

from typing import NamedTuple, List, Dict

from google.cloud import datastore


class UserConfig(NamedTuple):
    filter_regexps: List[str]
    ignore_channels: List[str]
    ignore_users: List[str]
    ignore_bots: List[str]

    @staticmethod
    def from_entity(entity: datastore.Entity):
        return UserConfig.from_json(entity)

    @staticmethod
    def from_json(json: Dict):
        def _get_or_empty(dic: Dict, key: str):
            return dic[key] if key in dic else []

        return UserConfig(
            _get_or_empty(json, 'filter_regexps'),
            _get_or_empty(json, 'ignore_channels'),
            _get_or_empty(json, 'ignore_users'),
            _get_or_empty(json, 'ignore_bots')
        )

    def update_entity(self, entity: datastore.Entity):
        entity.update(self.to_dict())

    def to_dict(self) -> Dict:
        return {
            'filter_regexps': self.filter_regexps,
            'ignore_channels': self.ignore_channels,
            'ignore_users': self.ignore_users,
            'ignore_bots': self.ignore_bots,
        }
