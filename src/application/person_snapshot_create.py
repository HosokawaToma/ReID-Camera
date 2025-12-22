import asyncio

from domain.frame import DomainFrame
from dto.frame_numpy import DtoFrameNumpy
from environment import Environment
from error import Error
from repository.admin_token import RepositoryAdminToken
from repository.person_snapshot_create import (
    RepositoryPersonSnapshotCreate,
    RepositoryPersonSnapshotCreateUnauthorizedError)


class ApplicationPersonSnapshotCreateError(Error):
    pass


class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        admin_token: RepositoryAdminToken,
        person_snapshot: RepositoryPersonSnapshotCreate,
    ):
        self.admin_token = admin_token
        self.person_snapshot = person_snapshot
        self.token = None
        self.token_lock = asyncio.Lock()

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotCreate":
        return cls(
            RepositoryAdminToken.create(environment),
            RepositoryPersonSnapshotCreate.create(environment),
        )

    async def handle(self, frame: DtoFrameNumpy) -> None:
        try:
            async with self.token_lock:
                if self.token is None:
                    self.token = await self.admin_token.request()
        except Error as error:
            raise ApplicationPersonSnapshotCreateError(error)
        try:
            await self.person_snapshot.create_by_frame(
                self.token,
                DomainFrame.create_from_numpy(frame.image, frame.timestamp)
            )
        except RepositoryPersonSnapshotCreateUnauthorizedError as error:
            try:
                async with self.token_lock:
                    self.token = await self.admin_token.request()
                await self.person_snapshot.create_by_frame(
                    self.token,
                    DomainFrame.create_from_numpy(frame.image, frame.timestamp)
                )
            except Error as try_error:
                raise ApplicationPersonSnapshotCreateError(try_error)
        except Error as error:
            raise ApplicationPersonSnapshotCreateError(error)
