from dataclasses import dataclass
from typing import List

import numpy as np

from modules.yolo.model import ModuleYoloBoundingBox, ModuleYoloDetections


@dataclass
class ModuleYoloCropPerson:
    bounding_box: ModuleYoloBoundingBox
    cropped_image: np.ndarray

class ModuleYoloCropFrame:
    def crop(self, frame: np.ndarray, detection: ModuleYoloDetections) -> ModuleYoloCropPerson:
        person_cropped_image = frame[
            detection.bounding_box.y1:detection.bounding_box.y2,
            detection.bounding_box.x1:detection.bounding_box.x2,
        ]
        return ModuleYoloCropPerson(detection.bounding_box, person_cropped_image)

    def crops(self, frame: np.ndarray, detections: List[ModuleYoloDetections]) -> list[ModuleYoloCropPerson]:
        person_cropped_images = []
        for detection in detections:
            person_cropped_image = self.crop(frame, detection)
            person_cropped_images.append(person_cropped_image)
        return person_cropped_images
