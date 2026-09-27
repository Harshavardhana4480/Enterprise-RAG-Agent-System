from loguru import logger
from openai import OpenAI

from config.settings import Settings
from src.voice.voice_errors import SpeechToTextError

client = OpenAI(api_key = Settings.OPENAI_API_KEY)

def transcribe_audio(audio_file_path: str) -> str:
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcribtion = client.audio.transcriptions.create(model = "gpt-4o-mini-transcribe", file = audio_file)
        text = transcribtion.text.strip()
        if not text:

            logger.warning(
                "Speech-to-text returned an empty transcription."
            )

            return ""
        logger.info("Speech-to-text transcription completed successfully.")
        return text
    
    except Exception as error:

        logger.exception(
            f"STT failed: {error}"
        )

        raise SpeechToTextError(
            "Speech transcription failed."
        ) from error

