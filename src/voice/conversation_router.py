from loguru import logger

CONFIDENCE_THRESHOLD = 0.70


class ConversationRouter:

    def route(self, intent: str, confidence: float) -> str:

        logger.info(
            f"Routing intent={intent}, "
            f"confidence={confidence:.2f}"
        )

        if confidence < CONFIDENCE_THRESHOLD:

            return "UNKNOWN"

        if intent == "GREETING":

            return "GREETING"

        if intent == "RAG_QUERY":

            return "RAG"

        if intent == "FOLLOW_UP":

            return "RAG"

        if intent == "REQUEST_HUMAN":

            return "HUMAN_HANDOFF"

        if intent == "GOODBYE":

            return "GOODBYE"

        return "UNKNOWN"