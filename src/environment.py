import os
from dataclasses import dataclass, field

import dotenv

dotenv.load_dotenv()


@dataclass
class Environment:

    camera_index: int = field(init=False)
    api_base_url: str = field(init=False)
    api_id: str = field(init=False)
    api_password: str = field(init=False)
    api_camera_id: int = field(init=False)
    api_view_id: int = field(init=False)
    ssl_verify: bool = field(init=False)

    def __post_init__(self):
        self.camera_index = self.get_int_value("CAMERA_INDEX")
        self.api_base_url = self.get_string_value("API_BASE_URL")
        self.api_id = self.get_string_value("API_ID")
        self.api_password = self.get_string_value("API_PASSWORD")
        self.api_camera_id = self.get_int_value("API_CAMERA_ID")
        self.api_view_id = self.get_int_value("API_VIEW_ID")
        self.ssl_verify = self.get_bool_value("SSL_VERIFY")

    def get_string_value(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise Exception(
                f"Environment variable '{key}' is not set. Please set it in your .env file or environment.")
        return value

    def get_int_value(self, key: str) -> int:
        value = os.getenv(key)
        if value is None:
            raise Exception(f"{key} is not set. Please set it in your .env file or environment.")
        try:
            return int(value)
        except ValueError:
            raise Exception(
                f"Environment variable '{key}' is not a valid integer. Please set it in your .env file or environment.")

    def get_bool_value(self, key: str) -> bool:
        value = os.getenv(key)
        if value is None:
            raise Exception(f"{key} is not set. Please set it in your .env file or environment.")
        if value.lower() not in ["true", "false"]:
            raise Exception(f"Environment variable '{key}' is not a valid boolean. Please set it in your .env file or environment.")
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        raise Exception(f"Environment variable '{key}' is not a valid boolean. Please set it in your .env file or environment.")
