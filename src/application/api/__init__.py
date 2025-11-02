import requests


class ApplicationApi:
    BASE_URL = None
    CAMERA_CLIENT_ID = None
    CAMERA_CLIENT_PASSWORD = None
    TOKEN = None
    HEADER = None
    LOGIN_URI = "/login/camera_client"
    CLIENT_ID_KEY_ON_REQUEST = "camera_client_id"
    PASSWORD_KEY_ON_REQUEST = "camera_client_password"
    TOKEN_KEY_ON_RESPONSE = "token"
    HEADER_AUTHORIZATION_KEY = "Authorization"
    HEADER_AUTHORIZATION_FORMAT = "Bearer {token}"

    def __init__(self, base_url: str, camera_client_id: str, camera_client_password: str):
        if self.BASE_URL is None:
            self.BASE_URL = base_url
        if self.CAMERA_CLIENT_ID is None:
            self.CAMERA_CLIENT_ID = camera_client_id
        if self.CAMERA_CLIENT_PASSWORD is None:
            self.CAMERA_CLIENT_PASSWORD = camera_client_password
        self.TOKEN = self._login()
        self.HEADER = {
            self.HEADER_AUTHORIZATION_KEY: self.HEADER_AUTHORIZATION_FORMAT.format(token=self.TOKEN)
        }

    def _login(self) -> str:
        response = requests.post(
            self.BASE_URL + self.LOGIN_URI,
            json={
                self.CLIENT_ID_KEY_ON_REQUEST: self.CAMERA_CLIENT_ID,
                self.PASSWORD_KEY_ON_REQUEST: self.CAMERA_CLIENT_PASSWORD,
            },
        )
        if response.status_code != 200:
            raise Exception("Failed to login")
        json = response.json()
        if self.TOKEN_KEY_ON_RESPONSE not in json:
            raise Exception("Failed to login")
        token = json[self.TOKEN_KEY_ON_RESPONSE]
        if token is None:
            raise Exception("Failed to login")
        if not isinstance(token, str):
            raise Exception("Failed to login")
        return token
