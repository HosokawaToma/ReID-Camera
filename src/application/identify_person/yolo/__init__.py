import numpy as np

from application.identify_person.yolo.crop_frame import \
    ApplicationIdentifyPersonYoloCropFrame
from application.identify_person.yolo.detections_verifier import \
    ApplicationIdentifyPersonYoloDetectionsVerifier
from application.identify_person.yolo.model import \
    ApplicationIdentifyPersonYoloModel
from entities.yolo.crop_person import EntityYoloCropPerson


class ApplicationIdentifyPersonYolo:
    def __init__(
        self,
        model: ApplicationIdentifyPersonYoloModel = ApplicationIdentifyPersonYoloModel(),
        verifier: ApplicationIdentifyPersonYoloDetectionsVerifier = ApplicationIdentifyPersonYoloDetectionsVerifier(),
        cropper: ApplicationIdentifyPersonYoloCropFrame = ApplicationIdentifyPersonYoloCropFrame(),
    ):
        self.model = model
        self.verifier = verifier
        self.cropper = cropper

    def crop_persons(self, frame: np.ndarray) -> list[EntityYoloCropPerson]:
        detections = self.model.extract_person_detections(frame)
        detections = self.verifier.verify(detections)
        return self.cropper.crops(frame, detections)
