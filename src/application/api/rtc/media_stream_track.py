import asyncio
import fractions
import time

import numpy as np
from aiortc import MediaStreamError, MediaStreamTrack
from av import VideoFrame


class ApplicationAPIRtcMediaStreamTrack(MediaStreamTrack):
    def __init__(
        self,
        audio_ptime: float,
        video_clock_rate: int,
        video_ptime: float,
        video_time_base: fractions.Fraction
    ):
        super().__init__()
        self.audio_ptime = audio_ptime
        self.video_clock_rate = video_clock_rate
        self.video_ptime = video_ptime
        self.video_time_base = video_time_base
        self._start = time.time()
        self._timestamp = 0
        self.frames: list[VideoFrame] = []

    async def _next_timestamp(self) -> int:
        self._timestamp += int(self.video_ptime * self.video_clock_rate)
        wait = self._start + (self._timestamp / self.video_clock_rate) - time.time()
        await asyncio.sleep(wait)
        return self._timestamp

    async def recv(self) -> VideoFrame:
        if len(self.frames) == 0:
            raise MediaStreamError("No frames available")
        return self.frames.pop(0)

    async def put_frame(self, frame: np.ndarray):
        pts = await self._next_timestamp()
        frame = VideoFrame.from_ndarray(frame, format="bgr24")
        frame.pts = pts
        frame.time_base = self.video_time_base
        self.frames.append(frame)
