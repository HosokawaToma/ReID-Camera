from typing import List

from entities.yolo.bounding_box import EntityYoloBoundingBox
from entities.yolo.detections import EntityYoloDetections


class ApplicationIdentifyPersonYoloDetectionsVerifier:
    def __init__(self, margin: int = 50):
        self.margin = margin

    def verify(self, person_detections: List[EntityYoloDetections]) -> List[EntityYoloDetections]:
        return_person_detections = []

        for person_detection in person_detections:
            if self._is_out_of_frame(person_detection.bounding_box, 1920, 1080):
                continue
            return_person_detections.append(person_detection)

        return return_person_detections

    def _is_out_of_frame(self, box: EntityYoloBoundingBox, image_width: int, image_height: int) -> bool:
        return (box.x1 <= self.margin or
                box.y1 <= self.margin or
                box.x2 >= (image_width - self.margin) or
                box.y2 >= (image_height - self.margin))
