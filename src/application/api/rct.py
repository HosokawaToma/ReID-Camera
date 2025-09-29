import aiohttp
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack


class ApplicationApiRct:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.rct_url = "https://" + self.server_ip + "/rct"
        self.rct_offer_url = "https://" + self.server_ip + "/rct/offer"
        self.rct_answer_url = "https://" + self.server_ip + "/rct/answer"
        self.rtc_peer_connection = RTCPeerConnection()
        self.video_track = VideoStreamTrack()
        self.rtc_peer_connection.addTrack(self.video_track)
        self.session = aiohttp.ClientSession()
        payload = {
            "sdp": self.rtc_peer_connection.localDescription.sdp,
            "type": self.rtc_peer_connection.localDescription.type
        }
        response = self.session.post(self.rct_offer_url, json=payload)
        if response.status != 200:
            raise Exception("Failed to connect to RCT server")
        response = self.session.get(self.rct_answer_url)
        if response.status != 200:
            raise Exception("Failed to get RCT server")
        params = response.json()
        self.session_description = RTCSessionDescription(
            sdp=params["sdp"], type=params["type"])
        self.rtc_peer_connection.setRemoteDescription(self.session_description)

    async def send_frame(self, frame: np.ndarray):
        await self.video_track.put_frame(frame)
