from pathlib import Path

from loguru import logger
from playsound import playsound


def play_audio(audio_path: str) -> None:

    audio_file = Path(audio_path)

    if not audio_file.exists():

        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    logger.info(f"Playing audio file: {audio_path}")

    try:
        playsound(str(audio_file))
        logger.info("Finished playing audio file")

    except Exception as e:
        logger.error(f"Error occurred while playing audio file: {e}")
        raise