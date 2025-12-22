import asyncio
import datetime

import requests

from environment import Environment
from error import Error


class RepositoryAdminTokenError(Error):
    pass


class RepositoryAdminTokenNotFoundError(RepositoryAdminTokenError):
    pass


class RepositoryAdminTokenIsNoneError(RepositoryAdminTokenError):
    pass


class RepositoryAdminTokenIsNotStringError(RepositoryAdminTokenError):
    pass


class RepositoryAdminTokenRequestFailedError(RepositoryAdminTokenError):
    pass


class RepositoryAdminToken:
    LOGIN_URI = "/api/v1/admin/auth/login"
    ID_KEY_ON_REQUEST = "id"
    PASSWORD_KEY_ON_REQUEST = "password"
    TOKEN_KEY_ON_RESPONSE = "token"
    EXPIRE_MINUTES = 15

    def __init__(self, base_url: str, id: str, password: str, ssl_verify: bool):
        self.token = None
        self._token_lock = asyncio.Lock()
        self._base_url = base_url
        self._id = id
        self._password = password
        self._ssl_verify = ssl_verify

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryAdminToken":
        return cls(
            base_url=environment.api_base_url,
            id=environment.api_id,
            password=environment.api_password,
            ssl_verify=environment.ssl_verify,
        )

    async def request(self) -> str:
        return await asyncio.to_thread(self._request)

    def _request(self) -> str:
        try:
            response = requests.post(
                f"{self._base_url}{self.LOGIN_URI}",
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    self.ID_KEY_ON_REQUEST: self._id,
                    self.PASSWORD_KEY_ON_REQUEST: self._password,
                },
                verify=self._ssl_verify,
            )
        except requests.exceptions.RequestException as error:
            raise RepositoryAdminTokenRequestFailedError(error)
        if response.status_code != 200:
            raise RepositoryAdminTokenRequestFailedError()
        json = response.json()
        if self.TOKEN_KEY_ON_RESPONSE not in json:
            raise RepositoryAdminTokenNotFoundError()
        token = json[self.TOKEN_KEY_ON_RESPONSE]
        if token is None:
            raise RepositoryAdminTokenIsNoneError()
        if not isinstance(token, str):
            raise RepositoryAdminTokenIsNotStringError()
        self.token = token
        return token
