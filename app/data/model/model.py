from typing import NamedTuple


class DatastoreConfig(NamedTuple):
    kind: str
    id: str  # key of user config in datastore.
