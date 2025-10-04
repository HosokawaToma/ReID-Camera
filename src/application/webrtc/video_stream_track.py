import asyncio

import av
import cv2
from aiortc import VideoStreamTrack


class ApplicationWebRTCVideoStreamTrack(VideoStreamTrack):
    def __init__(self, track: cv2.VideoCapture):
        self.track = track
        super().__init__()

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.track.read()
        if not ret:
            await asyncio.sleep(0.1)
            return await self.recv()
        video_frame = av.VideoFrame.from_ndarray(frame, format="bgr24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame
