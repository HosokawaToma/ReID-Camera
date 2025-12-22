import datetime
import time
from typing import Generator

import cv2

from dto.frame_numpy import DtoFrameNumpy
from environment import Environment
from error import Error


class ApplicationCameraError(Error):
    pass

class ApplicationCameraReadError(ApplicationCameraError):
    pass


class ApplicationCamera:
    def __init__(
        self,
        camera: cv2.VideoCapture,
    ):
        self.camera = camera

    @classmethod
    def create(cls, environment: Environment):
        return cls(cv2.VideoCapture(environment.camera_index))

    def read(self) -> Generator[DtoFrameNumpy, None, None]:
        while True:
            ret, image = self.camera.read()
            if not ret:
                raise ApplicationCameraReadError()
            yield DtoFrameNumpy(image, datetime.datetime.now())
