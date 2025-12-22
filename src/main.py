import asyncio

from application.camera import ApplicationCamera
from application.person_snapshot_create import ApplicationPersonSnapshotCreate
from environment import Environment
from error import Error
from logger import Logger


class CameraApp:
    def __init__(
        self,
        logger: Logger,
        camera: ApplicationCamera,
        person_snapshot_create: ApplicationPersonSnapshotCreate,
    ):
        self.logger = logger
        self.camera = camera
        self.person_snapshot_create = person_snapshot_create

    @classmethod
    def create(cls, environment: Environment):
        return cls(
            logger=Logger("main"),
            camera=ApplicationCamera.create(environment),
            person_snapshot_create=ApplicationPersonSnapshotCreate.create(
                environment),
        )

    async def run(self):
        while True:
            try:
                await self.handle()
            except Error as error:
                self.logger.error(error)
            except Exception as exception:
                self.logger.unexpected_error(exception)

    async def handle(self):
        for frame in self.camera.read():
            asyncio.create_task(self._handle_frame(frame))
            await asyncio.sleep(0.033)

    async def _handle_frame(self, frame):
        try:
            await self.person_snapshot_create.handle(frame)
        except Error as error:
            self.logger.error(error)
        except Exception as exception:
            self.logger.unexpected_error(exception)


def main():
    app = CameraApp.create(Environment())
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
