import re

from loguru import logger


def normalize_voice_input(text:str) -> str:
    if not text:
        logger.warning("Received empty voice input.")
        return ""

    normalized_text = text.strip()

    normalized_text = re.sub(r'\s+', ' ', normalized_text)

    logger.info("Normalized voice input")  
    return normalized_text