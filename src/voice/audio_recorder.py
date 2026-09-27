from pathlib import Path

import sounddevice as sd
from loguru import logger
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
CHANNELS = 1


def record_audio(
    duration: int = 5,
    output_path: str = "data/audio/user_input.wav"
) -> str:

    if duration <= 0:

        raise ValueError(
            "Recording duration must be greater than zero."
        )

    output_file = Path(output_path)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        f"Starting audio recording for {duration} seconds."
    )

    try:

        recording = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16"
        )

        sd.wait()

        write(
            output_file,
            SAMPLE_RATE,
            recording
        )

        logger.info(
            f"Audio recording completed: {output_file}"
        )

        return str(output_file)

    except Exception as error:

        logger.exception(
            f"Audio recording failed: {error}"
        )

        raise