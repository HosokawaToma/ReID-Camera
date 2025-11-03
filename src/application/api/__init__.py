import requests


class ApplicationApi:
    TOKEN = None
    LOGIN_URI = "/login/camera_client"
    CLIENT_ID_KEY_ON_REQUEST = "camera_client_id"
    PASSWORD_KEY_ON_REQUEST = "password"
    TOKEN_KEY_ON_RESPONSE = "token"
    HEADER_AUTHORIZATION_KEY = "Authorization"
    HEADER_AUTHORIZATION_FORMAT = "Bearer {token}"

    def __init__(self, base_url: str, camera_client_id: str, camera_client_password: str):
        self.base_url = base_url
        self.camera_client_id = camera_client_id
        self.camera_client_password = camera_client_password
        if not self.TOKEN:
            self.TOKEN = self._login()
        self.header = {
            self.HEADER_AUTHORIZATION_KEY: self.HEADER_AUTHORIZATION_FORMAT.format(token=self.TOKEN)
        }

    def _login(self) -> str:
        response = requests.post(
            self.base_url + self.LOGIN_URI,
            headers={
                "Content-Type": "application/json",
            },
            json={
                self.CLIENT_ID_KEY_ON_REQUEST: self.camera_client_id,
                self.PASSWORD_KEY_ON_REQUEST: self.camera_client_password,
            },
            verify=False,
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
