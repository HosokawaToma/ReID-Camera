import asyncio
from asyncio import Queue

import numpy as np


class RepositoryPersonCropQueue:
    _queue: Queue[np.ndarray] = Queue()

    async def put(self, crop: np.ndarray):
        await RepositoryPersonCropQueue._queue.put(crop)

    async def get(self) -> np.ndarray | None:
        try:
            return await RepositoryPersonCropQueue._queue.get()
        except asyncio.CancelledError:
            return None
