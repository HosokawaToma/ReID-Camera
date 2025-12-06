import datetime
from dataclasses import dataclass

import requests


class RepositoryApiPersonSnapshotCreateError(Exception):
    pass

class RepositoryApiPersonSnapshotCreateNotSuccessfulError(RepositoryApiPersonSnapshotCreateError):
    pass

class RepositoryApiPersonSnapshotCreateUnauthorizedError(RepositoryApiPersonSnapshotCreateNotSuccessfulError):
    pass

@dataclass
class RepositoryApiPersonSnapshotCreateParams:
    token: str
    image_bytes: bytes

class RepositoryApiPersonSnapshotCreate:
    PERSON_SNAPSHOT_CREATE_URI = "/api/v1/person/snapshot/create"
    IMAGE_KEY = "image"
    IMAGE_NAME = "image.jpg"
    IMAGE_CONTENT_TYPE = "image/jpeg"
    TIMESTAMP_KEY = "timestamp"

    def __init__(self, base_url: str):
        self.base_url = base_url

    def request(self, params: RepositoryApiPersonSnapshotCreateParams) -> None:
        image = [(self.IMAGE_KEY, (self.IMAGE_NAME, params.image_bytes, self.IMAGE_CONTENT_TYPE))]
        data = {
            self.TIMESTAMP_KEY: datetime.datetime.now().isoformat(),
        }
        try:
            response = requests.post(
                f"{self.base_url}{self.PERSON_SNAPSHOT_CREATE_URI}",
                headers={
                    "Authorization": f"Bearer {params.token}",
                },
                files=image,
                data=data,
                verify=False,
            )
        except requests.exceptions.RequestException:
            raise RepositoryApiPersonSnapshotCreateError()
        if response.status_code == 401:
            raise RepositoryApiPersonSnapshotCreateUnauthorizedError()
        if response.status_code != 200:
            raise RepositoryApiPersonSnapshotCreateNotSuccessfulError()
