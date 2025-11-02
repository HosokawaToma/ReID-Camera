import requests

from application.api import ApplicationApi
from entities.rtc.sdp import EntityRTCSdp


class ApplicationRTCConnection:
    RTC_CONNECTION_URI = "/rtc/connection"
    SDP_KEY = "sdp"
    TYPE_KEY = "type"

    def __init__(self, api: ApplicationApi):
        self.api = api

    def post(self, sdp: EntityRTCSdp) -> EntityRTCSdp:
        response = requests.post(
            f"{self.api.BASE_URL}{self.RTC_CONNECTION_URI}",
            headers=self.api.HEADER,
            json={
                self.SDP_KEY: sdp.sdp,
                self.TYPE_KEY: sdp.type,
            },
        )
        if response.status_code != 200:
            raise Exception("Failed to post RTC connection")
        json = response.json()
        if self.SDP_KEY not in json:
            raise Exception("Failed to post RTC connection")
        if self.TYPE_KEY not in json:
            raise Exception("Failed to post RTC connection")
        return EntityRTCSdp(
            sdp=json[self.SDP_KEY],
            type=json[self.TYPE_KEY],
        )
