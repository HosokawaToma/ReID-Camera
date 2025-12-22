import asyncio

from environment import Environment
from presentation.camera import PresentationCamera
from presentation.person_crop_create import PresentationPersonCropCreate
from presentation.person_snapshot_create import \
    PresentationPersonSnapshotCreate


class CameraApp:
    def __init__(
        self,
        camera: PresentationCamera,
        person_crop_create: PresentationPersonCropCreate,
        person_snapshot_create: PresentationPersonSnapshotCreate,
    ):
        self.camera = camera
        self.person_crop_create = person_crop_create
        self.person_snapshot_create = person_snapshot_create

    @classmethod
    def create(cls, environment: Environment):
        return cls(
            camera=PresentationCamera.create(environment),
            person_crop_create=PresentationPersonCropCreate.create(),
            person_snapshot_create=PresentationPersonSnapshotCreate.create(
                environment),
        )

    async def run(self):
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    async def setup(self):
        self.camera.setup()
        self.person_crop_create.setup()
        self.person_snapshot_create.setup()


async def main():
    app = CameraApp.create(Environment())
    await app.setup()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
