import cv2

from environment import Environment
from error import Error
from repository.frame_queue import RepositoryFrameQueue


class ApplicationCameraReadError(Error):
    pass


class ApplicationCamera:
    def __init__(
        self,
        camera: cv2.VideoCapture,
        frame_queue: RepositoryFrameQueue,
    ):
        self.camera = camera
        self.frame_queue = frame_queue

    @classmethod
    def create(cls, environment: Environment):
        return cls(cv2.VideoCapture(environment.camera_index), RepositoryFrameQueue())

    async def read(self) -> None:
        ret, frame = self.camera.read()
        if not ret:
            raise ApplicationCameraReadError("Failed to read frame from camera")
        await self.frame_queue.put(frame)
