import asyncio

import av
import numpy as np
from aiortc import VideoStreamTrack


class ApplicationRTCVideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        self.send_frames: asyncio.Queue[np.ndarray] = asyncio.Queue()
        super().__init__()

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        frame = await self.send_frames.get()
        if frame is None:
            await asyncio.sleep(0.1)
            return await self.recv()
        video_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

    def send_frame(self, frame: np.ndarray):
        self.send_frames.put_nowait(frame)
