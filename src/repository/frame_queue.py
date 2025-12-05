import asyncio

import numpy as np


class RepositoryFrameQueue:
    _queue: asyncio.Queue[np.ndarray] = asyncio.Queue()

    async def put(self, frame: np.ndarray):
        await RepositoryFrameQueue._queue.put(frame)

    async def get(self) -> np.ndarray | None:
        try:
            return await RepositoryFrameQueue._queue.get()
        except asyncio.CancelledError:
            return None
