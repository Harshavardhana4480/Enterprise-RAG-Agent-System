from pathlib import Path
from uuid import uuid4

from loguru import logger
from openai import OpenAI

from config.settings import Settings

client = OpenAI(
    api_key=Settings.OPENAI_API_KEY
)


def generate_speech(text: str, output_path: str = "data/audio/response.mp3") -> str:

    if not text or not text.strip():

        logger.warning(
            "Text-to-speech generation received empty text input."
        )

        raise ValueError(
            "Text input for text-to-speech generation cannot be empty."
        )

    output_file = Path(output_path)

    # Create a unique filename for every response
    output_file = (
        output_file.parent
        / f"{output_file.stem}_{uuid4().hex[:8]}{output_file.suffix}"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:

            response.stream_to_file(
                output_file
            )

        logger.info(
            "Text-to-speech generation completed successfully. "
            f"Audio saved to: {output_file}"
        )

        return str(output_file)

    except Exception as e:

        logger.exception(
            f"Text-to-speech generation failed: {e}"
        )

        raise