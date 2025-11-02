from dataclasses import dataclass

from entities.yolo.bounding_box import EntityYoloBoundingBox


@dataclass
class EntityYoloDetections:
    bounding_box: EntityYoloBoundingBox
    confidence: float
    cls: int
