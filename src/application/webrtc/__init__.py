import asyncio

import cv2

from application.webrtc.configuration import ApplicationWebRTCConfiguration
from application.webrtc.peer_connection import ApplicationWebRTCPeerConnection
from application.webrtc.video_stream_track import \
    ApplicationWebRTCVideoStreamTrack


class ApplicationWebRTC:
    def __init__(self, camera: cv2.VideoCapture, server_ip: str, token: str, turn_username: str, turn_password: str):
        self.camera = camera
        self.server_ip = server_ip
        self.token = token
        self.configuration = ApplicationWebRTCConfiguration(
            server_ip=server_ip,
            turn_username=turn_username,
            turn_password=turn_password,
        )
        self.media_stream_track = ApplicationWebRTCVideoStreamTrack(camera)
        self.peer_connection = ApplicationWebRTCPeerConnection(
            server_ip=server_ip,
            token=token,
            media_stream_track=self.media_stream_track,
            configuration=self.configuration,
        )

    async def start_streaming(self):
        await self.peer_connection.connect()
        while self.peer_connection.is_connected():
            await asyncio.sleep(1)
