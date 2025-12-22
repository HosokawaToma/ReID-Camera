import datetime
from dataclasses import dataclass

import numpy as np


@dataclass
class DtoFrameNumpy:
    image: np.ndarray
    timestamp: datetime.datetime
