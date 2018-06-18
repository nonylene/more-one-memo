"""
Common models.
"""

from typing import NamedTuple, List, Dict, Any

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
        def _check_items(items: Any, name: str):
            items_type = type(items)
            if items_type != list:
                raise TypeError(f'{name} type should be list or empty but got {items_type}.')

            for item in items:
                item_type = type(item)
                if item_type != str:
                    raise TypeError(f'Item in {name} type should be str but got {item_type}.')

        def _get_or_empty(dic: Dict, key: str):
            item = dic[key] if key in dic else []
            _check_items(item, key)
            return item

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
