import datetime

import numpy as np
import requests

from modules.image import ModuleImage


class ApplicationApiIdentifyPerson:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.person_cropped_images_url = "https://" + self.server_ip + "/identify_person"

    def post_person_cropped_images(self, person_cropped_images: list[np.ndarray], camera_id: int, view_id: int):
        if len(person_cropped_images) == 0:
            return
        files = []
        for i, person_cropped_image in enumerate(person_cropped_images):
            image_bytes = ModuleImage.encode_image(person_cropped_image)
            files.append(
                ("images", (f"person_cropped_image_{i}.jpg", image_bytes, "image/jpeg")))
        data = {
            "camera_id": camera_id,
            "view_id": view_id,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }
        requests.post(self.person_cropped_images_url, files=files, data=data, verify=False)
