class HandoffContextBuilder:

    def build_context(
        self,
        history: list,
        current_question: str,
        reason: str
    ) -> dict:

        return {

            "reason": reason,

            "current_question":
                current_question,

            "conversation_history":
                history
        }