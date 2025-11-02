import requests

from application.api import ApplicationApi
from entities.rtc.ice_server import EntityRTCIceServer


class ApplicationRTCIceServer:
    RTC_ICE_SERVER_URI = "/rtc/ice_server"
    URLS_KEY = "urls"
    USERNAME_KEY = "username"
    CREDENTIAL_KEY = "credential"

    def __init__(self, api: ApplicationApi):
        self.api = api

    def get(self) -> EntityRTCIceServer:
        response = requests.get(
            f"{self.api.base_url}{self.RTC_ICE_SERVER_URI}",
            headers=self.api.header,
        )
        if response.status_code != 200:
            raise Exception("Failed to get ICE server")
        json = response.json()
        if self.URLS_KEY not in json:
            raise Exception("Failed to get ICE server")
        if self.USERNAME_KEY not in json:
            raise Exception("Failed to get ICE server")
        if self.CREDENTIAL_KEY not in json:
            raise Exception("Failed to get ICE server")
        return EntityRTCIceServer(
            urls=json[self.URLS_KEY],
            username=json[self.USERNAME_KEY],
            credential=json[self.CREDENTIAL_KEY],
        )
