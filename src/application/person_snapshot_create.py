from environment import Environment
from modules.image import ModuleImage
from repository.api.auth.login.camera_client import (
    RepositoryApiAuthLoginCameraClient,
    RepositoryApiAuthLoginCameraClientError)
from repository.api.person.snapshot.create import (
    RepositoryApiPersonSnapshotCreate,
    RepositoryApiPersonSnapshotCreateNotSuccessfulError,
    RepositoryApiPersonSnapshotCreateParams,
    RepositoryApiPersonSnapshotCreateUnauthorizedError)
from repository.person_crop_queue import RepositoryPersonCropQueue


class ApplicationPersonSnapshotCreateError(Exception):
    pass

class ApplicationPersonSnapshotCreatePersonSnapshotCreateApiError(ApplicationPersonSnapshotCreateError):
    pass

class ApplicationPersonSnapshotCreateAuthLoginApiError(ApplicationPersonSnapshotCreateError):
    pass

class ApplicationPersonSnapshotCreatePersonCropQueueError(ApplicationPersonSnapshotCreateError):
    pass

class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        person_crop_queue: RepositoryPersonCropQueue,
        image: ModuleImage,
        auth_login_camera_client: RepositoryApiAuthLoginCameraClient,
        person_snapshot_create: RepositoryApiPersonSnapshotCreate,
    ):
        self.person_crop_queue = person_crop_queue
        self.image = image
        self.auth_login_camera_client = auth_login_camera_client
        self.person_snapshot_create = person_snapshot_create
        self.token = None

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotCreate":
        return cls(
            RepositoryPersonCropQueue(),
            ModuleImage(),
            RepositoryApiAuthLoginCameraClient(
                base_url=environment.api_base_url,
                client_id=environment.api_camera_client_id,
                password=environment.api_password,
            ),
            RepositoryApiPersonSnapshotCreate(base_url=environment.api_base_url),
        )

    async def handle(self) -> None:
        try:
            if self.token is None:
                self.token = self.auth_login_camera_client.request()
        except RepositoryApiAuthLoginCameraClientError:
            raise ApplicationPersonSnapshotCreateAuthLoginApiError
        crop = await self.person_crop_queue.get()
        if crop is None:
            raise ApplicationPersonSnapshotCreatePersonCropQueueError
        image_bytes = self.image.encode(crop)
        try:
            self.person_snapshot_create.request(
                RepositoryApiPersonSnapshotCreateParams(
                    token=self.token,
                    image_bytes=image_bytes,
                ),
            )
        except RepositoryApiPersonSnapshotCreateUnauthorizedError:
            self.token = None
            await self.person_crop_queue.put(crop)
            raise ApplicationPersonSnapshotCreateAuthLoginApiError
        except RepositoryApiPersonSnapshotCreateNotSuccessfulError:
            await self.person_crop_queue.put(crop)
            raise ApplicationPersonSnapshotCreatePersonSnapshotCreateApiError
