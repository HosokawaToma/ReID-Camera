from application.camera import ApplicationCamera
from environment import Environment
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
    def create(cls, environment: Environment):
        return cls(
            logger=PresentationLogger(),
            application=ApplicationCamera.create(environment),
        )

    async def handle(self) -> None:
        await self.application.read()
