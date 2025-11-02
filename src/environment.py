import os


class Environment:
    CAMERA_INDEX = "CAMERA_INDEX"
    API_BASE_URL = "API_BASE_URL"
    API_CAMERA_CLIENT_ID = "API_CAMERA_CLIENT_ID"
    API_PASSWORD = "API_PASSWORD"

    def get_camera_index(self):
        value = os.getenv(self.CAMERA_INDEX)
        if value is None:
            raise Exception(f"{self.CAMERA_INDEX} is not set")
        try:
            return int(value)
        except ValueError:
            raise Exception(f"{self.CAMERA_INDEX} is not a valid integer")

    def get_api_base_url(self):
        value = os.getenv(self.API_BASE_URL)
        if value is None:
            raise Exception(f"{self.API_BASE_URL} is not set")
        return value

    def get_api_camera_client_id(self):
        value = os.getenv(self.API_CAMERA_CLIENT_ID)
        if value is None:
            raise Exception(f"{self.API_CAMERA_CLIENT_ID} is not set")
        return value

    def get_api_camera_password(self):
        value = os.getenv(self.API_PASSWORD)
        if value is None:
            raise Exception(f"{self.API_PASSWORD} is not set")
        return value
