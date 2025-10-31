import io

import cv2
import numpy as np
import requests
import datetime
from PIL import Image

from entities.environment.api import EntitiesEnvironmentApi


class ApplicationApiIdentifyPerson:
    IDENTIFY_PERSON_URI = "/identify_person"
    IMAGES_KEY = "images"
    IMAGE_NAME_FORMAT = "{i}.jpg"
    IMAGE_CONTENT_TYPE = "image/jpeg"
    TIMESTAMP_KEY = "timestamp"


    def __init__(self, environment: EntitiesEnvironmentApi):
        self.environment = environment
        self.token = None

    def request(self, image_bytes_list: list[bytes]) -> None:
        images = [
            (self.IMAGES_KEY, (self.IMAGE_NAME_FORMAT.format(i=i), image_bytes, self.IMAGE_CONTENT_TYPE))
            for i, image_bytes in enumerate[bytes](image_bytes_list)
        ]
        data = {
            self.TIMESTAMP_KEY: self.now_timestamp(),
        }
        requests.post(
            self.environment.base_url + self.IDENTIFY_PERSON_URI,
            files=images,
            data=data,
            verify=False,
            headers=self.environment.header.update({
                self.environment.HEADER_AUTHORIZATION_KEY: self.environment.HEADER_AUTHORIZATION_FORMAT.format(token=self.token)
            }),
        )

    def encode_image(self, image: np.ndarray) -> bytes:
        if image.dtype != np.uint8:
            image = (
                image * 255).astype(np.uint8)
        image_rgb = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image_rgb)
        buffer = io.BytesIO()
        image_bytes = buffer.getvalue()
        return image_bytes

    def now_timestamp(self) -> str:
        return datetime.datetime.now().isoformat()
