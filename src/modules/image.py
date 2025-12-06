import io

import cv2
import numpy as np
from PIL import Image


class ModuleImage:
    def encode(self, image: np.ndarray) -> bytes:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil: Image.Image = Image.fromarray(image_rgb)
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        return image_bytes
