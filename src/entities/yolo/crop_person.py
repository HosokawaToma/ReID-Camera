from dataclasses import dataclass

import numpy as np

from entities.yolo.bounding_box import EntityYoloBoundingBox


@dataclass
class EntityYoloCropPerson:
    bounding_box: EntityYoloBoundingBox
    cropped_image: np.ndarray
