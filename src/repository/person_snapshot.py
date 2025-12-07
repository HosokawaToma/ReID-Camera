import datetime
from dataclasses import dataclass

import requests

from error import Error


class RepositoryPersonSnapshotCreateError(Error):
    pass

@dataclass
class RepositoryPersonSnapshotCreateParams:
    token: str
    image_bytes: bytes

class RepositoryPersonSnapshotCreate:
    PERSON_SNAPSHOT_CREATE_URI = "/api/v1/person/snapshot/create"
    IMAGE_KEY = "image"
    IMAGE_NAME = "image.jpg"
    IMAGE_CONTENT_TYPE = "image/jpeg"
    TIMESTAMP_KEY = "timestamp"

    def __init__(self, base_url: str):
        self.base_url = base_url

    def request(self, params: RepositoryPersonSnapshotCreateParams) -> None:
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
            raise RepositoryPersonSnapshotCreateError("Failed to request person snapshot create")
        if response.status_code != 200:
            raise RepositoryPersonSnapshotCreateError("Request failed with status code: " + str(response.status_code))
