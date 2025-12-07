import asyncio

import numpy as np


class RepositoryFrameQueue:
    _queue: asyncio.Queue[np.ndarray] | None = None

    async def put(self, frame: np.ndarray):
        if RepositoryFrameQueue._queue is None:
            RepositoryFrameQueue._queue = asyncio.Queue()
        await RepositoryFrameQueue._queue.put(frame)

    async def get(self) -> np.ndarray | None:
        if RepositoryFrameQueue._queue is None:
            return None
        try:
            return await RepositoryFrameQueue._queue.get()
        except asyncio.CancelledError:
            return None
