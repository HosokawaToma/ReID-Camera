import requests

from entities.environment.api import EntitiesEnvironmentApi


class ApplicationApiLogin:
    LOGIN_URI = "/login"
    CLIENT_ID_KEY_ON_REQUEST = "client_id"
    PASSWORD_KEY_ON_REQUEST = "password"
    TOKEN_KEY_ON_RESPONSE = "token"

    def __init__(self, environment: EntitiesEnvironmentApi):
        self.environment = environment
        self.token = None

    def request(self) -> str:
        response = requests.post(
            self.environment.base_url + self.LOGIN_URI,
            json={
                self.CLIENT_ID_KEY_ON_REQUEST: self.environment.client_id,
                self.PASSWORD_KEY_ON_REQUEST: self.environment.password,
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
