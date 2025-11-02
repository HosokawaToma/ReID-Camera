import datetime
import io

import cv2
import numpy as np
import requests
from PIL import Image

from application.api import ApplicationApi


class ApplicationApiIdentifyPerson:
    IDENTIFY_PERSON_URI = "/identify_person"
    IMAGES_KEY = "images"
    IMAGE_NAME_FORMAT = "{i}.jpg"
    IMAGE_CONTENT_TYPE = "image/jpeg"
    TIMESTAMP_KEY = "timestamp"


    def __init__(self, api: ApplicationApi):
        self.api = api

    def request(self, image_bytes_list: list[bytes]) -> None:
        images = [
            (self.IMAGES_KEY, (self.IMAGE_NAME_FORMAT.format(i=i), image_bytes, self.IMAGE_CONTENT_TYPE))
            for i, image_bytes in enumerate[bytes](image_bytes_list)
        ]
        data = {
            self.TIMESTAMP_KEY: self.now_timestamp(),
        }
        requests.post(
            self.api.base_url + self.IDENTIFY_PERSON_URI,
            headers=self.api.header,
            files=images,
            data=data,
            verify=False,
        )

    def encode_image(self, image: np.ndarray) -> bytes:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil: Image.Image = Image.fromarray(image_rgb)
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        return image_bytes

    def now_timestamp(self) -> str:
        return datetime.datetime.now().isoformat()
