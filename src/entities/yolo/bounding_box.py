from dataclasses import dataclass


@dataclass
class EntityYoloBoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int
    width: int
    height: int
