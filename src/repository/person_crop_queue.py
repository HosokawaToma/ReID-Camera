import asyncio

import numpy as np


class RepositoryPersonCropQueue:
    _queue: asyncio.Queue[np.ndarray] | None = None

    async def put(self, crop: np.ndarray):
        if RepositoryPersonCropQueue._queue is None:
            RepositoryPersonCropQueue._queue = asyncio.Queue()
        await RepositoryPersonCropQueue._queue.put(crop)

    async def get(self) -> np.ndarray | None:
        if RepositoryPersonCropQueue._queue is None:
            return None
        try:
            return await RepositoryPersonCropQueue._queue.get()
        except asyncio.CancelledError:
            return None
