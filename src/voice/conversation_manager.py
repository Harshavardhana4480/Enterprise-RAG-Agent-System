from loguru import logger

from src.agents.memory import MemoryAgent

MAX_CONTEXT_TURNS = 5


class ConversationManager:

    def __init__(self):

        self.memory = MemoryAgent()

    def get_context(self, question: str) -> str:

        history = self.memory.get_recent_history(
            limit=MAX_CONTEXT_TURNS
        )

        if not history:

            return question

        context_lines = []

        for item in history:

            context_lines.append(
                f"Previous Question: "
                f"{item['question']}"
            )

            context_lines.append(
                f"Previous Answer: "
                f"{item['answer']}"
            )

        context = "\n".join(
            context_lines
        )

        contextual_question = (
            "Conversation history:\n"
            f"{context}\n\n"
            "Current user question:\n"
            f"{question}"
        )

        logger.info(
            "Conversation context generated."
        )

        return contextual_question

    def add_turn(
        self,
        question: str,
        answer: str
    ) -> None:

        self.memory.add_message(
            question,
            answer
        )
    def get_history(self) -> list:

        return self.memory.get_history()
    
    def clear_memory(self) -> None:

        self.memory.clear()