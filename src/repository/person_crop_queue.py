import asyncio

import numpy as np


class RepositoryPersonCropQueue:
    _queue: asyncio.Queue[np.ndarray] = asyncio.Queue()

    async def put(self, crop: np.ndarray):
        await RepositoryPersonCropQueue._queue.put(crop)

    async def get(self) -> np.ndarray | None:
        try:
            return await RepositoryPersonCropQueue._queue.get()
        except asyncio.CancelledError:
            return None
