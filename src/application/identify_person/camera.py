import cv2


class ApplicationIdentifyPersonCamera:
    def __init__(self, camera: cv2.VideoCapture):
        self.camera = camera

    def run(self):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                return
            yield frame
