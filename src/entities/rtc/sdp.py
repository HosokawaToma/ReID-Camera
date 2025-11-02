from dataclasses import dataclass

@dataclass
class EntityRTCSdp:
    sdp: str
    type: str
