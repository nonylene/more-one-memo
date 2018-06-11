"""
Common models.
"""

from typing import NamedTuple, List

from google.cloud import datastore


class UserConfig(NamedTuple):
    filter_regexps: List[str]
    ignore_channels: List[str]
    ignore_users: List[str]
    ignore_bots: List[str]

    @staticmethod
    def from_entity(entity: datastore.Entity):
        def _get_or_empty(e: datastore.Entity, key: str):
            return e[key] if key in e else []

        return UserConfig(
            _get_or_empty(entity, 'filter_regexps'),
            _get_or_empty(entity, 'ignore_channels'),
            _get_or_empty(entity, 'ignore_users'),
            _get_or_empty(entity, 'ignore_bots')
        )

    def update_entity(self, entity: datastore.Entity):
        entity['filter_regexps'] = self.filter_regexps
        entity['ignore_channels'] = self.ignore_channels
        entity['ignore_users'] = self.ignore_users
        entity['ignore_bots'] = self.ignore_bots
