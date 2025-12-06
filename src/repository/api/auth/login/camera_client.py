import requests


class RepositoryApiAuthLoginCameraClientError(Exception):
    pass


class RepositoryApiAuthLoginCameraClientNotSuccessfulError(RepositoryApiAuthLoginCameraClientError):
    pass


class RepositoryApiAuthLoginCameraClientTokenNotFoundError(RepositoryApiAuthLoginCameraClientError):
    pass


class RepositoryApiAuthLoginCameraClient:
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
            raise RepositoryApiAuthLoginCameraClientError()
        if response.status_code != 200:
            raise RepositoryApiAuthLoginCameraClientNotSuccessfulError()
        json = response.json()
        if self.TOKEN_KEY_ON_RESPONSE not in json:
            raise RepositoryApiAuthLoginCameraClientTokenNotFoundError()
        token = json[self.TOKEN_KEY_ON_RESPONSE]
        if token is None:
            raise RepositoryApiAuthLoginCameraClientTokenNotFoundError()
        if not isinstance(token, str):
            raise RepositoryApiAuthLoginCameraClientTokenNotFoundError()
        return token
