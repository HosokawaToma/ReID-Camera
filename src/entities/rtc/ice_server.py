from dataclasses import dataclass


@dataclass
class EntityRTCIceServer:
    urls: list[str]
    username: str
    credential: str
