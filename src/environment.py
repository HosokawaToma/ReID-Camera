import os


class Environment:
    API_SERVER_IP_KEY = "API_SERVER_IP"
    API_PORT_KEY = "API_PORT"
    API_CLIENT_ID_KEY = "API_CLIENT_ID"
    API_PASSWORD_KEY = "API_PASSWORD"
    COTURN_USERNAME_KEY = "COTURN_USERNAME"
    COTURN_PASSWORD_KEY = "COTURN_PASSWORD"
    CAMERA_INDEX_KEY = "CAMERA_INDEX"

    def get_camera_index(self):
        value = os.getenv(self.CAMERA_INDEX_KEY)
        if value is None:
            raise Exception(f"{self.CAMERA_INDEX_KEY} is not set")
        return int(value)

    def get_api_server_ip(self):
        value = os.getenv(self.API_SERVER_IP_KEY)
        if value is None:
            raise Exception(f"{self.API_SERVER_IP_KEY} is not set")
        return value

    def get_api_port(self):
        value = os.getenv(self.API_PORT_KEY)
        if value is None:
            raise Exception(f"{self.API_PORT_KEY} is not set")
        return value

    def get_api_client_id(self):
        value = os.getenv(self.API_CLIENT_ID_KEY)
        if value is None:
            raise Exception(f"{self.API_CLIENT_ID_KEY} is not set")
        return value

    def get_api_password(self):
        value = os.getenv(self.API_PASSWORD_KEY)
        if value is None:
            raise Exception(f"{self.API_PASSWORD_KEY} is not set")
        return value

    def get_coturn_username(self):
        value = os.getenv(self.COTURN_USERNAME_KEY)
        if value is None:
            raise Exception(f"{self.COTURN_USERNAME_KEY} is not set")
        return value

    def get_coturn_password(self):
        value = os.getenv(self.COTURN_PASSWORD_KEY)
        if value is None:
            raise Exception(f"{self.COTURN_PASSWORD_KEY} is not set")
        return value
