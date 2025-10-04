from typing import List

import numpy as np

from entities.yolo.crop_person import EntityYoloCropPerson
from entities.yolo.detections import EntityYoloDetections


class ApplicationIdentifyPersonYoloCropFrame:
    def crop(self, frame: np.ndarray, detection: EntityYoloDetections) -> EntityYoloCropPerson:
        person_cropped_image = frame[
            detection.bounding_box.y1:detection.bounding_box.y2,
            detection.bounding_box.x1:detection.bounding_box.x2,
        ]
        return EntityYoloCropPerson(detection.bounding_box, person_cropped_image)

    def crops(self, frame: np.ndarray, detections: List[EntityYoloDetections]) -> list[EntityYoloCropPerson]:
        person_cropped_images = []
        for detection in detections:
            person_cropped_image = self.crop(frame, detection)
            person_cropped_images.append(person_cropped_image)
        return person_cropped_images
