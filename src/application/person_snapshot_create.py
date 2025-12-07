import asyncio

from environment import Environment
from error import Error
from modules.image import ModuleImage
from repository.camera_client_token import (RepositoryCameraClientToken,
                                            RepositoryCameraClientTokenError)
from repository.person_crop_queue import RepositoryPersonCropQueue
from repository.person_snapshot import (RepositoryPersonSnapshotCreate,
                                        RepositoryPersonSnapshotCreateError,
                                        RepositoryPersonSnapshotCreateParams)


class ApplicationPersonSnapshotCreateError(Error):
    pass

class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        person_crop_queue: RepositoryPersonCropQueue,
        image: ModuleImage,
        camera_client_token: RepositoryCameraClientToken,
        person_snapshot_create: RepositoryPersonSnapshotCreate,
    ):
        self.person_crop_queue = person_crop_queue
        self.image = image
        self.camera_client_token = camera_client_token
        self.person_snapshot_create = person_snapshot_create
        self._token_lock = asyncio.Lock()
        self._token = None

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotCreate":
        return cls(
            RepositoryPersonCropQueue(),
            ModuleImage(),
            RepositoryCameraClientToken(
                base_url=environment.api_base_url,
                client_id=environment.api_camera_client_id,
                password=environment.api_password,
            ),
            RepositoryPersonSnapshotCreate(base_url=environment.api_base_url),
        )

    async def handle(self) -> None:
        try:
            async with self._token_lock:
                if self._token is None:
                    self._token = await asyncio.to_thread(self.camera_client_token.request)
        except RepositoryCameraClientTokenError as e:
            raise ApplicationPersonSnapshotCreateError(e.message)

        crop = await self.person_crop_queue.get()
        if crop is None:
            raise ApplicationPersonSnapshotCreateError("Failed to get crop from person crop queue")
        image_bytes = self.image.encode(crop)

        try:
            await asyncio.to_thread(self.person_snapshot_create.request,
                RepositoryPersonSnapshotCreateParams(
                    token=self._token,
                    image_bytes=image_bytes,
                ),
            )
        except RepositoryPersonSnapshotCreateError as e:
            self.token = None
            await self.person_crop_queue.put(crop)
            raise ApplicationPersonSnapshotCreateError(e.message)
