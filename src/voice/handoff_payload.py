from datetime import datetime, timezone


class HandoffPayloadBuilder:

    def build_payload(
        self,
        session_id: str,
        reason: str,
        current_question: str,
        conversation_history: list
    ) -> dict:

        return {

            "session_id":
                session_id,

            "handoff_reason":
                reason,

            "current_question":
                current_question,

            "conversation_history":
                conversation_history,

            "created_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "status":
                "PENDING"
        }