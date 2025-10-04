import datetime
import io

import cv2
import numpy as np
import requests
from PIL import Image


class ApplicationIdentifyPersonApi:
    def __init__(self, server_ip: str, token: str):
        self.server_ip = server_ip
        self.token = token
        self.person_cropped_images_url = "https://" + self.server_ip + "/identify_person"
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def post(self, person_cropped_images: list[np.ndarray]):
        if len(person_cropped_images) == 0:
            return
        files = []
        for i, person_cropped_image in enumerate(person_cropped_images):
            image_bytes = self._encode_image(person_cropped_image)
            files.append(
                ("images", (f"person_cropped_image_{i}.jpg", image_bytes, "image/jpeg")))
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        requests.post(self.person_cropped_images_url, files=files,
                      data=data, verify=False, headers=self.headers)

    def _encode_image(self, image: np.ndarray) -> bytes:
        if image.dtype != np.uint8:
            image = (
                image * 255).astype(np.uint8)
        image_rgb = cv2.cvtColor(
            image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image_rgb)
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        return image_bytes
