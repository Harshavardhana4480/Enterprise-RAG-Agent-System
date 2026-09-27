from loguru import logger


class MemoryAgent:

    def __init__(self):

        self.history = []

    def add_message(self, question: str, answer: str) -> None:

        self.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        logger.info("Conversation memory updated.")

    def get_history(self) -> list:

        return self.history

    def get_recent_history(self, limit: int = 5 ) -> list:

        return self.history[-limit:]

    def clear(self) -> None:

        self.history = []

        logger.info(
            "Conversation memory cleared."
        )