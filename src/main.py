import asyncio

import cv2

from application.api.identify_person import ApplicationApiIdentifyPerson
from application.api.login import ApplicationApiLogin
from application.webrtc import ApplicationWebRTC
from application.yolo import ApplicationYolo
from entities.environment.api import EntitiesEnvironmentApi
from environment import Environment


class CameraApp:
    def __init__(
        self,
        camera: cv2.VideoCapture,
        yolo: ApplicationYolo,
        login: ApplicationApiLogin,
        webrtc: ApplicationWebRTC,
        identify_person: ApplicationApiIdentifyPerson,
    ):
        self.camera = camera
        self.yolo = yolo
        self.login = login
        self.webrtc = webrtc
        self.identify_person = identify_person

    @classmethod
    def create(cls):
        environment = Environment()
        environment_api = EntitiesEnvironmentApi(
            server_ip=environment.get_api_server_ip(),
            port=environment.get_api_port(),
            client_id=environment.get_api_client_id(),
            password=environment.get_api_password(),
        )
        return cls(
            camera=cv2.VideoCapture(environment.get_camera_index()),
            yolo=ApplicationYolo.create(),
            login=ApplicationApiLogin(environment_api),
            webrtc=ApplicationWebRTC(environment_api),
            identify_person=ApplicationApiIdentifyPerson(environment_api),
        )

    async def run(self):
        token = self.login.request()
        self.identify_person.token = token
        self.webrtc.token = token
        streaming_task = asyncio.create_task(self.webrtc.start_streaming())
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to read frame from camera")
                    break
                yolo_crop_persons = self.yolo.crop_persons(frame)
                self.webrtc.send_frame(frame)
                image_bytes_list = [
                    self.identify_person.encode_image(person.cropped_image)
                    for person in yolo_crop_persons
                    ]
                self.identify_person.request(image_bytes_list)
                await asyncio.sleep(0.033)
        except KeyboardInterrupt:
            print("Application is shutting down...")
        finally:
            print("Streaming task cancelled")
            streaming_task.cancel()


if __name__ == "__main__":
    app = CameraApp()
    asyncio.run(app.run())
