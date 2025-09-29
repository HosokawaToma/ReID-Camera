import numpy as np

from application.yolo.crop_frame import ApplicationYoloCropFrame
from application.yolo.detections_verifier import \
    ApplicationYoloDetectionsVerifier
from application.yolo.model import ApplicationYoloModel
from entities.yolo.crop_person import EntityYoloCropPerson


class ApplicationYolo:
    def __init__(
        self,
        model: ApplicationYoloModel = ApplicationYoloModel(),
        verifier: ApplicationYoloDetectionsVerifier = ApplicationYoloDetectionsVerifier(),
        cropper: ApplicationYoloCropFrame = ApplicationYoloCropFrame(),
    ):
        self.model = model
        self.verifier = verifier
        self.cropper = cropper

    def crop_persons(self, frame: np.ndarray) -> list[EntityYoloCropPerson]:
        detections = self.model.extract_person_detections(frame)
        detections = self.verifier.verify(detections)
        return self.cropper.crops(frame, detections)
