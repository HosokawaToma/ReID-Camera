import numpy as np

from modules.yolo.crop_frame import ModuleYoloCropFrame, ModuleYoloCropPerson
from modules.yolo.model import ModuleYoloModel


class ModuleYolo:
    def __init__(
        self,
        model: ModuleYoloModel,
        cropper: ModuleYoloCropFrame,
    ):
        self.model = model
        self.cropper = cropper

    @classmethod
    def create(cls):
        return cls(
            model=ModuleYoloModel(),
            cropper=ModuleYoloCropFrame(),
        )

    def extract(self, frame: np.ndarray) -> list[ModuleYoloCropPerson]:
        detections = self.model.extract_person_detections(frame)
        return self.cropper.crops(frame, detections)
