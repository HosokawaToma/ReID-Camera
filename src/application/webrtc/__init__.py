import asyncio

import numpy as np

from application.webrtc.configuration import ApplicationWebRTCConfiguration
from application.webrtc.peer_connection import ApplicationWebRTCPeerConnection
from application.webrtc.video_stream_track import \
    ApplicationWebRTCVideoStreamTrack


class ApplicationWebRTC:
    def __init__(self, server_ip: str, token: str, turn_username: str, turn_password: str):
        self.server_ip = server_ip
        self.token = token
        self.configuration = ApplicationWebRTCConfiguration(
            server_ip=server_ip,
            turn_username=turn_username,
            turn_password=turn_password,
        )
        self.media_stream_track = ApplicationWebRTCVideoStreamTrack()
        self.peer_connection = ApplicationWebRTCPeerConnection(
            server_ip=server_ip,
            token=token,
            media_stream_track=self.media_stream_track,
            configuration=self.configuration,
        )

    async def start_streaming(self):
        print("Starting streaming")
        await self.peer_connection.connect()
        while self.peer_connection.is_connected():
            await asyncio.sleep(1)

    def send_frame(self, frame: np.ndarray):
        self.media_stream_track.send_frame(frame)
