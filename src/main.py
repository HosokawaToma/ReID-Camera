import asyncio

import cv2

from application.api import ApplicationApi
from application.environment import ApplicationEnvironment
from application.identify_person import ApplicationIdentifyPerson
from application.webrtc import ApplicationWebRTC


class CameraApp:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.environment = ApplicationEnvironment()
        self.server_ip = self.environment.get_api_server_ip()
        self.api_client_id = self.environment.get_api_client_id()
        self.api_password = self.environment.get_api_password()
        self.webrtc_turn_username = self.environment.get_webrtc_turn_username()
        self.webrtc_turn_password = self.environment.get_webrtc_turn_password()
        self.api = ApplicationApi(
            server_ip=self.environment.get_api_server_ip(),
        )
        self.token = self.api.login(
            client_id=self.environment.get_api_client_id(),
            password=self.environment.get_api_password(),
        )
        if self.token is None:
            raise Exception("Failed to login")
        self.webrtc = ApplicationWebRTC(
            camera=self.camera,
            server_ip=self.server_ip,
            token=self.token,
            turn_username=self.webrtc_turn_username,
            turn_password=self.webrtc_turn_password,
        )
        self.identify_person = ApplicationIdentifyPerson(
            server_ip=self.environment.get_api_server_ip(),
            token=self.token,
            camera=self.camera,
        )

    async def run(self):
        asyncio.gather(
            self.webrtc.start_streaming(),
            self.identify_person.run(),
        )

if __name__ == "__main__":
    app = CameraApp()
    asyncio.run(app.run())
