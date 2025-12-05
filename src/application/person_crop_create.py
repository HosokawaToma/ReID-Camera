
import logging

from modules.yolo import ModuleYolo
from repository.frame_queue import RepositoryFrameQueue
from repository.person_crop_queue import RepositoryPersonCropQueue

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ApplicationPersonCropCreate:
    def __init__(
        self,
        module_yolo: ModuleYolo,
        frame_queue: RepositoryFrameQueue,
        person_crop_queue: RepositoryPersonCropQueue,
    ):
        self.module_yolo = module_yolo
        self.frame_queue = frame_queue
        self.person_crop_queue = person_crop_queue

    @classmethod
    def create(cls):
        return cls(ModuleYolo.create(), RepositoryFrameQueue(), RepositoryPersonCropQueue())

    async def handle(self) -> None:
        frame = await self.frame_queue.get()
        if frame is None:
            return
        person_detections = self.module_yolo.extract(frame)
        if len(person_detections) == 0:
            return
        for person_detection in person_detections:
            await self.person_crop_queue.put(person_detection.cropped_image)
