import requests

from error import Error


class RepositoryCameraClientTokenError(Error):
    pass


class RepositoryCameraClientToken:
    LOGIN_URI = "/api/v1/auth/login/camera_client"
    CLIENT_ID_KEY_ON_REQUEST = "camera_client_id"
    PASSWORD_KEY_ON_REQUEST = "password"
    TOKEN_KEY_ON_RESPONSE = "token"

    def __init__(self, base_url: str, client_id: str, password: str):
        self.base_url = base_url
        self.client_id = client_id
        self.password = password

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
                verify=False,
            )
        except requests.exceptions.RequestException:
            raise RepositoryCameraClientTokenError("Failed to request camera client token")
        if response.status_code != 200:
            raise RepositoryCameraClientTokenError("Request failed with status code: " + str(response.status_code))
        json = response.json()
        if self.TOKEN_KEY_ON_RESPONSE not in json:
            raise RepositoryCameraClientTokenError("Token not found in response")
        token = json[self.TOKEN_KEY_ON_RESPONSE]
        if token is None:
            raise RepositoryCameraClientTokenError("Token is None")
        if not isinstance(token, str):
            raise RepositoryCameraClientTokenError("Token is not a string")
        return token
