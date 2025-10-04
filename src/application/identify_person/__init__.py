import numpy as np

from application.identify_person.api import ApplicationIdentifyPersonApi
from application.identify_person.yolo import ApplicationIdentifyPersonYolo


class ApplicationIdentifyPerson:
    def __init__(self, server_ip: str, token: str):
        self.server_ip = server_ip
        self.token = token
        self.yolo = ApplicationIdentifyPersonYolo()
        self.api = ApplicationIdentifyPersonApi(self.server_ip, self.token)

    def run(self, frame: np.ndarray):
        yolo_crop_persons = self.yolo.crop_persons(frame)
        person_cropped_images = [yolo_crop_person.cropped_image for yolo_crop_person in yolo_crop_persons]
        self.api.post(person_cropped_images)
