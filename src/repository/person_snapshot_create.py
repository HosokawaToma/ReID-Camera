import asyncio
import datetime
from dataclasses import dataclass

import requests

from domain.frame import DomainFrame
from environment import Environment
from error import Error


class RepositoryPersonSnapshotCreateError(Error):
    pass


class RepositoryPersonSnapshotCreateResponseError(RepositoryPersonSnapshotCreateError):
    pass


class RepositoryPersonSnapshotCreateUnauthorizedError(RepositoryPersonSnapshotCreateError):
    pass


class RepositoryPersonSnapshotCreateResponseStatusCodeNot200Error(RepositoryPersonSnapshotCreateError):
    pass


class RepositoryPersonSnapshotCreate:
    PERSON_SNAPSHOT_CREATE_URI = "/api/v1/person/snapshot/create"
    TIMESTAMP_KEY_ON_REQUEST = "timestamp"
    CAMERA_ID_KEY_ON_REQUEST = "camera_id"
    VIEW_ID_KEY_ON_REQUEST = "view_id"
    IMAGE_KEY_ON_REQUEST = "image"
    IMAGE_NAME = "image.jpg"
    IMAGE_CONTENT_TYPE = "image/jpeg"

    def __init__(self, base_url: str, camera_id: int, view_id: int, ssl_verify: bool):
        self.base_url = base_url
        self.camera_id = camera_id
        self.view_id = view_id
        self.ssl_verify = ssl_verify

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotCreate":
        return cls(
            base_url=environment.api_base_url,
            camera_id=environment.api_camera_id,
            view_id=environment.api_view_id,
            ssl_verify=environment.ssl_verify,
        )

    async def create_by_frame(self, token: str, frame: DomainFrame) -> None:
        return await asyncio.to_thread(self._request, token, frame)

    def _request(self, token: str, frame: DomainFrame) -> None:
        image = [
            (self.IMAGE_KEY_ON_REQUEST, (self.IMAGE_NAME, frame.to_bytes(), self.IMAGE_CONTENT_TYPE))]
        data = {
            self.TIMESTAMP_KEY_ON_REQUEST: datetime.datetime.now().isoformat(),
            self.CAMERA_ID_KEY_ON_REQUEST: self.camera_id,
            self.VIEW_ID_KEY_ON_REQUEST: self.view_id,
        }
        try:
            response = requests.post(
                f"{self.base_url}{self.PERSON_SNAPSHOT_CREATE_URI}",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                files=image,
                data=data,
                verify=self.ssl_verify,
            )
        except requests.exceptions.RequestException as error:
            raise RepositoryPersonSnapshotCreateResponseError(
                error)
        if response.status_code == 401:
            raise RepositoryPersonSnapshotCreateUnauthorizedError()
        if response.status_code != 200:
            raise RepositoryPersonSnapshotCreateResponseStatusCodeNot200Error()
