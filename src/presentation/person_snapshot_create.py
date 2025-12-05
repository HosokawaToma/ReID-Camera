from application.person_snapshot_create import ApplicationPersonSnapshotCreate
from environment import Environment
from presentation import PresentationBase, PresentationLogger


class PresentationPersonSnapshotCreate(PresentationBase):
    def __init__(
        self,
        logger: PresentationLogger,
        application: ApplicationPersonSnapshotCreate
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment):
        return cls(
            logger=PresentationLogger(),
            application=ApplicationPersonSnapshotCreate.create(environment),
        )

    async def handle(self) -> None:
        await self.application.handle()
