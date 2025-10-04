import asyncio

import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription

from application.webrtc.configuration import ApplicationWebRTCConfiguration
from application.webrtc.video_stream_track import \
    ApplicationWebRTCVideoStreamTrack


class ApplicationWebRTCPeerConnection:
    def __init__(
        self,
        server_ip: str,
        token: str,
        media_stream_track: ApplicationWebRTCVideoStreamTrack,
        configuration: ApplicationWebRTCConfiguration,
    ):
        self.server_ip = server_ip
        self.token = token
        self.connected = asyncio.Event()
        self.configuration = configuration
        self.media_stream_track = media_stream_track
        self.running = True

    async def connect(self):
        configuration = self.configuration.get_configuration()
        self.peer_connection = RTCPeerConnection(configuration=configuration)
        self.peer_connection.on("connectionstatechange", self._on_connectionstatechange)
        self.peer_connection.addTrack(self.media_stream_track)
        offer = await self.peer_connection.createOffer()
        await self.peer_connection.setLocalDescription(offer)
        async with aiohttp.ClientSession() as session:
            server_url = f"https://{self.server_ip}/rtc/offer"
            json = {
                "sdp": self.peer_connection.localDescription.sdp,
                "type": self.peer_connection.localDescription.type,
            }
            headers = {
                "Authorization": f"Bearer {self.token}",
            }
            async with session.post(server_url, json=json, headers=headers, ssl=False) as response:
                if response.status != 200:
                    return
                answer_data = await response.json()
                answer = RTCSessionDescription(
                    sdp=answer_data["sdp"], type=answer_data["type"])
                await self.peer_connection.setRemoteDescription(answer)
        await self.connected.wait()

    def _on_connectionstatechange(self):
        if self.peer_connection.connectionState == "connected":
            self.connected.set()
        elif self.peer_connection.connectionState in ["failed", "closed", "disconnected"]:
            self.connected.set()

    def is_connected(self):
        return self.peer_connection.connectionState == "connected"
