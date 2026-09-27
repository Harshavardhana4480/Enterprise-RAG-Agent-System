import uuid

from loguru import logger


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def create_session(self) -> str:

        session_id = str(
            uuid.uuid4()
        )

        self.sessions[session_id] = {

            "status": "ACTIVE",

            "turn_count": 0,

            "failed_attempts": 0,

            "unknown_intents": 0
        }

        logger.info(
            f"Voice session created: "
            f"{session_id}"
        )

        return session_id

    def get_session(
        self,
        session_id: str
    ) -> dict:

        if session_id not in self.sessions:

            raise ValueError(
                f"Session not found: "
                f"{session_id}"
            )

        return self.sessions[session_id]

    def update_turn(
        self,
        session_id: str
    ) -> None:

        session = self.get_session(
            session_id
        )

        session["turn_count"] += 1

        logger.info(
            f"Session {session_id} "
            f"updated to turn "
            f"{session['turn_count']}"
        )

    def increment_failed_attempts(
        self,
        session_id: str
    ) -> int:

        session = self.get_session(
            session_id
        )

        session["failed_attempts"] += 1

        return session[
            "failed_attempts"
        ]

    def increment_unknown_intents(
        self,
        session_id: str
    ) -> int:

        session = self.get_session(
            session_id
        )

        session["unknown_intents"] += 1

        return session[
            "unknown_intents"
        ]

    def reset_failures(
        self,
        session_id: str
    ) -> None:

        session = self.get_session(
            session_id
        )

        session["failed_attempts"] = 0

        session["unknown_intents"] = 0

    def end_session(
        self,
        session_id: str
    ) -> None:

        session = self.get_session(
            session_id
        )

        session["status"] = "ENDED"

        logger.info(
            f"Voice session ended: "
            f"{session_id}"
        )