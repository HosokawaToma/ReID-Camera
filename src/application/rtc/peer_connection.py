import asyncio

import numpy as np
from aiortc import (RTCConfiguration, RTCIceServer, RTCPeerConnection,
                    RTCSessionDescription)

from application.rtc.video_stream_track import ApplicationRTCVideoStreamTrack
from entities.rtc.ice_server import EntityRTCIceServer
from entities.rtc.sdp import EntityRTCSdp


class ApplicationWebRTCPeerConnection:
    def __init__(
        self,
        video_stream_track: ApplicationRTCVideoStreamTrack,
    ):
        self.peer_connection = None
        self.video_stream_track = video_stream_track
        self.connected = asyncio.Event()
        self.task = None

    def create_peer_connection(self, ice_server: EntityRTCIceServer):
        self.peer_connection = RTCPeerConnection(
            RTCConfiguration(
                iceServers=[
                    RTCIceServer(
                        urls=ice_server.urls,
                        username=ice_server.username,
                        credential=ice_server.credential,
                    ),
                ],
            ),
        )
        self.peer_connection.on("connectionstatechange",
                                self._on_connectionstatechange)
        self.peer_connection.addTrack(self.video_stream_track)

    async def set_local_description(self) -> EntityRTCSdp:
        if self.peer_connection is None:
            raise Exception("Peer connection is not created")
        offer = await self.peer_connection.createOffer()
        await self.peer_connection.setLocalDescription(offer)
        return EntityRTCSdp(
            sdp=self.peer_connection.localDescription.sdp,
            type=self.peer_connection.localDescription.type,
        )

    async def set_remote_description(self, sdp: EntityRTCSdp):
        if self.peer_connection is None:
            raise Exception("Peer connection is not created")
        await self.peer_connection.setRemoteDescription(RTCSessionDescription(
            sdp=sdp.sdp,
            type=sdp.type,
        ))

    async def start_streaming(self):
        while self.is_connected():
            await asyncio.sleep(1)

    async def wait_connected(self):
        await self.connected.wait()

    def send_frame(self, frame: np.ndarray):
        self.video_stream_track.send_frame(frame)

    def _on_connectionstatechange(self):
        if self.peer_connection is None:
            return
        if self.peer_connection.connectionState == "connected":
            self.connected.set()
        elif self.peer_connection.connectionState in ["failed", "closed", "disconnected"]:
            self.connected.clear()

    def is_connected(self):
        if self.peer_connection is None:
            return False
        return self.peer_connection.connectionState == "connected"
