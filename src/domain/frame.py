import datetime
import io
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image


@dataclass
class DomainFrame:
    image: Image.Image
    timestamp: datetime.datetime

    @classmethod
    def create_from_numpy(cls, image: np.ndarray, timestamp: datetime.datetime) -> "DomainFrame":
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil: Image.Image = Image.fromarray(image_rgb)
        return cls(image_pil, timestamp)

    def to_bytes(self) -> bytes:
        buffer = io.BytesIO()
        self.image.save(buffer, format="JPEG")
        return buffer.getvalue()
