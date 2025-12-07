import requests

from environment import Environment
from error import Error


class RepositoryCameraClientTokenCreateError(Error):
    pass


class RepositoryCameraClientTokenCreate:
    LOGIN_URI = "/api/v1/auth/login/camera_client"
    CLIENT_ID_KEY_ON_REQUEST = "camera_client_id"
    PASSWORD_KEY_ON_REQUEST = "password"
    TOKEN_KEY_ON_RESPONSE = "token"

    def __init__(self, base_url: str, client_id: str, password: str, ssl_verify: bool):
        self.base_url = base_url
        self.client_id = client_id
        self.password = password
        self.ssl_verify = ssl_verify

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryCameraClientTokenCreate":
        return cls(
            base_url=environment.api_base_url,
            client_id=environment.api_camera_client_id,
            password=environment.api_password,
            ssl_verify=environment.ssl_verify,
        )

    def request(self) -> str:
        try:
            response = requests.post(
                f"{self.base_url}{self.LOGIN_URI}",
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    self.CLIENT_ID_KEY_ON_REQUEST: self.client_id,
                    self.PASSWORD_KEY_ON_REQUEST: self.password,
                },
                verify=self.ssl_verify,
            )
        except requests.exceptions.RequestException:
            raise RepositoryCameraClientTokenCreateError("Failed to request camera client token")
        if response.status_code != 200:
            raise RepositoryCameraClientTokenCreateError("Request failed with status code: " + str(response.status_code))
        json = response.json()
        if self.TOKEN_KEY_ON_RESPONSE not in json:
            raise RepositoryCameraClientTokenCreateError("Token not found in response")
        token = json[self.TOKEN_KEY_ON_RESPONSE]
        if token is None:
            raise RepositoryCameraClientTokenCreateError("Token is None")
        if not isinstance(token, str):
            raise RepositoryCameraClientTokenCreateError("Token is not a string")
        return token
