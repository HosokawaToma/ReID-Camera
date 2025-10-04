import cv2

from application.identify_person.api import ApplicationIdentifyPersonApi
from application.identify_person.camera import ApplicationIdentifyPersonCamera
from application.identify_person.yolo import ApplicationIdentifyPersonYolo


class ApplicationIdentifyPerson:
    def __init__(self, server_ip: str, token: str, camera: cv2.VideoCapture):
        self.server_ip = server_ip
        self.token = token
        self.camera = camera
        self.camera = ApplicationIdentifyPersonCamera(self.camera)
        self.yolo = ApplicationIdentifyPersonYolo()
        self.api = ApplicationIdentifyPersonApi(self.server_ip, self.token)

    def run(self):
        for frame in self.camera.run():
            yolo_crop_persons = self.yolo.crop_persons(frame)
            person_cropped_images = [yolo_crop_person.cropped_image for yolo_crop_person in yolo_crop_persons]
            self.api.post(person_cropped_images)
