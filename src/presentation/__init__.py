import asyncio
import logging


class PresentationLogger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            self.logger.addHandler(logging.StreamHandler())

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)


class PresentationBase:
    def __init__(self, logger: PresentationLogger):
        self.logger = logger

    def setup(self) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.create_task(self.run())

    async def run(self) -> None:
        while True:
            try:
                await self.handle()
                await asyncio.sleep(0.033)
            except Exception as e:
                self.logger.error(f"Error: {e}")
                await asyncio.sleep(1)

    async def handle(self) -> None:
        pass
