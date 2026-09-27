from openai import OpenAI
from loguru import logger

from config.settings import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_answer(prompt):

    logger.info(
        f"Sending prompt to LLM. Prompt length: {len(prompt)}"
    )

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=settings.MAX_COMPLETION_TOKENS,
    )

    logger.info(
        f"LLM response received. "
        f"Finish reason: {response.choices[0].finish_reason}"
    )

    content = response.choices[0].message.content

    logger.info(
        f"LLM content type: {type(content)}"
    )

    logger.info(
        f"LLM content length: {len(content) if content else 0}"
    )

    logger.info(
        f"LLM content preview: {repr(content[:500]) if content else None}"
    )

    if not content or not content.strip():

        logger.warning(
            "LLM returned an empty response."
        )

        return (
            "I could not generate an answer from "
            "the uploaded documents."
        )

    return content.strip()