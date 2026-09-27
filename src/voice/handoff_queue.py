from loguru import logger


class HandoffQueue:

    def __init__(self):

        self.queue = []

    def add(
        self,
        handoff_payload: dict
    ) -> None:

        self.queue.append(
            handoff_payload
        )

        logger.info(
            "Handoff request added to queue."
        )

    def get_pending(self) -> list:

        return [

            item

            for item in self.queue

            if item["status"] == "PENDING"
        ]

    def assign(
        self,
        session_id: str,
        agent_name: str
    ) -> None:

        for item in self.queue:

            if (
                item["session_id"]
                == session_id
                and item["status"]
                == "PENDING"
            ):

                item["status"] = "ASSIGNED"

                item["assigned_agent"] = (
                    agent_name
                )

                logger.info(
                    f"Session {session_id} "
                    f"assigned to {agent_name}."
                )

                return

        raise ValueError(
            "Pending handoff request "
            "not found."
        )