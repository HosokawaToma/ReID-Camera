import os
from dataclasses import dataclass, field
import dotenv

dotenv.load_dotenv()


@dataclass
class Environment:

    camera_index: int = field(init=False)
    api_base_url: str = field(init=False)
    api_camera_client_id: str = field(init=False)
    api_password: str = field(init=False)

    def __post_init__(self):
        self.camera_index = self.get_int_value("CAMERA_INDEX")
        self.api_base_url = self.get_string_value("API_BASE_URL")
        self.api_camera_client_id = self.get_string_value("API_CAMERA_CLIENT_ID")
        self.api_password = self.get_string_value("API_PASSWORD")

    def get_string_value(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise Exception(f"{key} is not set")
        return value

    def get_int_value(self, key: str) -> int:
        value = os.getenv(key)
        if value is None:
            raise Exception(f"{key} is not set")
        try:
            return int(value)
        except ValueError:
            raise Exception(f"{key} is not a valid integer")
