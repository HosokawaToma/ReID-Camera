import aiohttp
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription

from application.api.rtc.media_stream_track import \
    ApplicationAPIRtcMediaStreamTrack


class ApplicationApiRtc:
    def __init__(self, server_ip: str):
        self.server_ip = server_ip
        self.rtc_url = "https://" + self.server_ip + "/rtc"
        self.rtc_offer_url = "https://" + self.server_ip + "/rtc/offer"
        self.rtc_answer_url = "https://" + self.server_ip + "/rtc/answer"
        self.rtc_peer_connection = RTCPeerConnection()
        self.video_track = ApplicationAPIRtcMediaStreamTrack()
        self.rtc_peer_connection.addTrack(self.video_track)
        self.session = aiohttp.ClientSession()
        payload = {
            "sdp": self.rtc_peer_connection.localDescription.sdp,
            "type": self.rtc_peer_connection.localDescription.type
        }
        response = self.session.post(self.rtc_offer_url, json=payload)
        if response.status != 200:
            raise Exception("Failed to connect to RTC server")
        response = self.session.get(self.rtc_answer_url)
        if response.status != 200:
            raise Exception("Failed to get RTC server")
        params = response.json()
        self.session_description = RTCSessionDescription(
            sdp=params["sdp"], type=params["type"])
        self.rtc_peer_connection.setRemoteDescription(self.session_description)

    async def put_frame(self, frame: np.ndarray):
        await self.video_track.put_frame(frame)
