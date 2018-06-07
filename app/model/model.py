"""
Common models.
"""

from typing import NamedTuple
from google.cloud import datastore


class UserConfig(NamedTuple):
    id: str

    @staticmethod
    def from_entity(entity: datastore.Entity):
        return UserConfig(entity["id"])
