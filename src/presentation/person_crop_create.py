from application.person_crop_create import ApplicationPersonCropCreate
from presentation import PresentationBase, PresentationLogger


class PresentationPersonCropCreate(PresentationBase):
    def __init__(
        self,
        logger: PresentationLogger,
        application: ApplicationPersonCropCreate
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls):
        return cls(
            logger=PresentationLogger(),
            application=ApplicationPersonCropCreate.create(),
        )

    async def handle(self) -> None:
        await self.application.handle()
