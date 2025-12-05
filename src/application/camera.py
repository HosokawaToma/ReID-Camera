import cv2

from repository.frame_queue import RepositoryFrameQueue


class ApplicationCameraReadError(Exception):
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
    def create(cls):
        return cls(cv2.VideoCapture(0), RepositoryFrameQueue())

    async def read(self) -> None:
        ret, frame = self.camera.read()
        if not ret:
            raise ApplicationCameraReadError
        await self.frame_queue.put(frame)
