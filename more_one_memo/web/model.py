from dataclasses import dataclass


@dataclass
class WebConfig:
    mongo_uri: str
    host: str
    port: int
