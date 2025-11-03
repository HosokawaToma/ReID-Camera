import asyncio
import time

import cv2

from application.api import ApplicationApi
from application.api.identify_person import ApplicationApiIdentifyPerson
from application.api.rtc.connection import ApplicationRTCConnection
from application.api.rtc.ice_server import ApplicationRTCIceServer
from application.rtc.peer_connection import ApplicationWebRTCPeerConnection
from application.rtc.video_stream_track import ApplicationRTCVideoStreamTrack
from application.yolo import ApplicationYolo
from entities.environment.api import EntitiesEnvironmentApi
from environment import Environment


class CameraApp:
    def __init__(
        self,
        camera: cv2.VideoCapture,
        yolo: ApplicationYolo,
        identify_person: ApplicationApiIdentifyPerson,
        rtc_ice_server: ApplicationRTCIceServer,
        rtc_connection: ApplicationRTCConnection,
        rtc_peer_connection: ApplicationWebRTCPeerConnection,
    ):
        self.camera = camera
        self.yolo = yolo
        self.identify_person = identify_person
        self.rtc_ice_server = rtc_ice_server
        self.rtc_connection = rtc_connection
        self.rtc_peer_connection = rtc_peer_connection

    @classmethod
    def create(cls, environment: Environment):
        environment_api = EntitiesEnvironmentApi(
            base_url=environment.get_api_base_url(),
            client_id=environment.get_api_camera_client_id(),
            password=environment.get_api_camera_password(),
        )
        api = ApplicationApi(
            base_url=environment_api.base_url,
            camera_client_id=environment_api.client_id,
            camera_client_password=environment_api.password,
        )
        return cls(
            camera=cv2.VideoCapture(environment.get_camera_index()),
            yolo=ApplicationYolo.create(),
            identify_person=ApplicationApiIdentifyPerson(api),
            rtc_ice_server=ApplicationRTCIceServer(api),
            rtc_connection=ApplicationRTCConnection(api),
            rtc_peer_connection=ApplicationWebRTCPeerConnection(
                video_stream_track=ApplicationRTCVideoStreamTrack(),
            ),
        )

    async def run(self):
        self.rtc_peer_connection.create_peer_connection(self.rtc_ice_server.get())
        local_description = await self.rtc_peer_connection.set_local_description()
        remote_description = self.rtc_connection.post(local_description)
        await self.rtc_peer_connection.set_remote_description(remote_description)
        streaming_task = asyncio.create_task(self.rtc_peer_connection.start_streaming())
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    break
                yolo_crop_persons = self.yolo.crop_persons(frame)
                self.rtc_peer_connection.send_frame(frame)
                image_bytes_list = [
                    self.identify_person.encode_image(person.cropped_image)
                    for person in yolo_crop_persons
                    ]
                self.identify_person.request(image_bytes_list)
                await asyncio.sleep(0.033)
        except KeyboardInterrupt:
            return
        finally:
            streaming_task.cancel()


if __name__ == "__main__":
    while True:
        try:
            app = CameraApp.create(Environment())
            asyncio.run(app.run())
        except Exception as e:
            print(e)
            time.sleep(60)
