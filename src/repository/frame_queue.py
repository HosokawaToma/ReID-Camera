import asyncio
from asyncio import Queue

import numpy as np


class RepositoryFrameQueue:
    _queue: Queue[np.ndarray] = Queue()

    async def put(self, frame: np.ndarray):
        await RepositoryFrameQueue._queue.put(frame)

    async def get(self) -> np.ndarray | None:
        try:
            return await RepositoryFrameQueue._queue.get()
        except asyncio.CancelledError:
            return None
