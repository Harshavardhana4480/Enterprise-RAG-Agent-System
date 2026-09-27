from loguru import logger


class PlaybackManager:

    def __init__(self):

        self.is_playing = False

    def start(self):

        self.is_playing = True

        logger.info(
            "Audio playback started."
        )

    def stop(self):

        if self.is_playing:

            logger.info(
                "Audio playback interrupted."
            )

        self.is_playing = False

    def status(self) -> bool:

        return self.is_playing