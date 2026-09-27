from loguru import logger

from src.voice.escalation_config import (
    HANDOFF_REASON_REPEATED_FAILURE,
    HANDOFF_REASON_UNKNOWN_INTENT,
    HANDOFF_REASON_USER_REQUEST,
    MAX_FAILED_ATTEMPTS,
    MAX_UNKNOWN_INTENTS,
)


class HandoffManager:

    def should_handoff(
        self,
        intent: str,
        failed_attempts: int = 0,
        unknown_intents: int = 0
    ) -> tuple[bool, str | None]:

        # ------------------------------------------
        # Explicit user request
        # ------------------------------------------

        if intent == "REQUEST_HUMAN":

            logger.info(
                "Human handoff requested by user."
            )

            return (
                True,
                HANDOFF_REASON_USER_REQUEST
            )

        # ------------------------------------------
        # Repeated failures
        # ------------------------------------------

        if failed_attempts >= MAX_FAILED_ATTEMPTS:

            logger.info(
                "Human handoff triggered by "
                "repeated failures."
            )

            return (
                True,
                HANDOFF_REASON_REPEATED_FAILURE
            )

        # ------------------------------------------
        # Repeated unknown intents
        # ------------------------------------------

        if unknown_intents >= MAX_UNKNOWN_INTENTS:

            logger.info(
                "Human handoff triggered by "
                "repeated unknown intents."
            )

            return (
                True,
                HANDOFF_REASON_UNKNOWN_INTENT
            )

        return (
            False,
            None
        )