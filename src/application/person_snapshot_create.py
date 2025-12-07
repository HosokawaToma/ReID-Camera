import asyncio

from environment import Environment
from error import Error
from modules.image import ModuleImage
from repository.camera_client_token_create import (RepositoryCameraClientTokenCreate,
                                                    RepositoryCameraClientTokenCreateError)
from repository.person_crop_queue import RepositoryPersonCropQueue
from repository.person_snapshot_create import (RepositoryPersonSnapshotCreate,
                                                RepositoryPersonSnapshotCreateError,
                                                RepositoryPersonSnapshotCreateParams)


class ApplicationPersonSnapshotCreateError(Error):
    pass

class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        person_crop_queue: RepositoryPersonCropQueue,
        image: ModuleImage,
        camera_client_token: RepositoryCameraClientTokenCreate,
        person_snapshot: RepositoryPersonSnapshotCreate,
    ):
        self.person_crop_queue = person_crop_queue
        self.image = image
        self.camera_client_token = camera_client_token
        self.person_snapshot = person_snapshot
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
            RepositoryCameraClientTokenCreate.create(environment),
            RepositoryPersonSnapshotCreate.create(environment),
        )

    async def handle(self) -> None:
        try:
            async with self._token_lock:
                if self._token is None:
                    self._token = await asyncio.to_thread(self.camera_client_token.request)
        except RepositoryCameraClientTokenCreateError as e:
            raise ApplicationPersonSnapshotCreateError(e.message)

        crop = await self.person_crop_queue.get()
        if crop is None:
            raise ApplicationPersonSnapshotCreateError("Failed to get crop from person crop queue")
        image_bytes = self.image.encode(crop)

        try:
            await asyncio.to_thread(self.person_snapshot.request,
                RepositoryPersonSnapshotCreateParams(
                    token=self._token,
                    image_bytes=image_bytes,
                ),
            )
        except RepositoryPersonSnapshotCreateError as e:
            async with self._token_lock:
                self._token = None
            await self.person_crop_queue.put(crop)
            raise ApplicationPersonSnapshotCreateError(e.message)
