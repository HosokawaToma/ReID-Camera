from application.api.identify_person import ApplicationApiIdentifyPerson
from application.api.rtc import ApplicationApiRtc
from application.camera import ApplicationCamera
from application.yolo import ApplicationYolo


class CameraApp:
    def __init__(self, camera_id: int = 0, view_id: int = 0):
        self.camera_id = camera_id
        self.view_id = view_id
        self.camera = ApplicationCamera()
        self.yolo = ApplicationYolo()
        self.api_identify_person = ApplicationApiIdentifyPerson(server_ip="133.89.36.10")
        #self.api_rtc = ApplicationApiRtc(server_ip="133.89.36.10")

    def run(self):
        for frame in self.camera.run():
            yolo_cropped_images = self.yolo.crop_persons(frame)
            person_cropped_images = [cropped_image.cropped_image for cropped_image in yolo_cropped_images]
            self.api_identify_person.post_person_cropped_images(person_cropped_images, self.camera_id, self.view_id)
            #self.api_rtc.put_frame(frame)

if __name__ == "__main__":
    app = CameraApp()
    app.run()
