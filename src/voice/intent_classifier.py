import json

from loguru import logger
from openai import OpenAI

from config.settings import settings
from src.voice.intent_config import INTENTS

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


INTENT_PROMPT = """
You are an intent classification component
for a conversational enterprise voice agent.

Classify the user's message into exactly one
of the following intents:

GREETING
RAG_QUERY
FOLLOW_UP
REQUEST_HUMAN
GOODBYE
UNKNOWN

Definitions:

GREETING:
The user is greeting the assistant.

RAG_QUERY:
The user is asking for information that may
require searching the enterprise documents.

FOLLOW_UP:
The user's question depends on previous
conversation context.

REQUEST_HUMAN:
The user explicitly wants to speak to or be
transferred to a human.

GOODBYE:
The user is ending the conversation.

UNKNOWN:
The message does not clearly belong to any
supported intent.

Return valid JSON with exactly these fields:

{{
    "intent": "INTENT_NAME",
    "confidence": "CONFIDENCE_SCORE"
}}

The confidence must be a number between
0.0 and 1.0.

User message:
{question}
"""


def classify_intent(question: str) -> dict:

    prompt = INTENT_PROMPT.format(
        question=question
    )

    try:

        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={
                "type": "json_object"
            }
        )

        response_text = response.choices[0].message.content.strip()

        result = json.loads(
            response_text
        )

        intent = result.get(
            "intent",
            "UNKNOWN"
        ).upper()

        confidence = float(
            result.get(
                "confidence",
                0.0
            )
        )

        if intent not in INTENTS:

            logger.warning(
                f"Invalid intent: {intent}"
            )

            return {
                "intent": "UNKNOWN",
                "confidence": 0.0
            }

        confidence = max(
            0.0,
            min(
                confidence,
                1.0
            )
        )

        logger.info(
            f"Intent: {intent}, "
            f"confidence: {confidence:.2f}"
        )

        return {
            "intent": intent,
            "confidence": confidence
        }

    except Exception as error:

        logger.exception(
            f"Intent classification failed: {error}"
        )

        return {
            "intent": "UNKNOWN",
            "confidence": 0.0
        }