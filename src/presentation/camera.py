from application.camera import ApplicationCamera
from presentation import PresentationBase, PresentationLogger


class PresentationCamera(PresentationBase):
    def __init__(
        self,
        logger: PresentationLogger,
        application: ApplicationCamera
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls):
        return cls(
            logger=PresentationLogger(),
            application=ApplicationCamera.create(),
        )

    async def handle(self) -> None:
        await self.application.read()
