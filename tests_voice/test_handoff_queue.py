from src.voice.handoff_queue import HandoffQueue

queue = HandoffQueue()


payload = {

    "session_id": "session-001",

    "handoff_reason":
        "USER_REQUEST",

    "current_question":
        "I want to speak to a human.",

    "conversation_history": [],

    "status":
        "PENDING"
}


queue.add(
    payload
)


print("\nPending:")
print(
    queue.get_pending()
)


queue.assign(
    "session-001",
    "HumanAgent-01"
)


print("\nAfter assignment:")
print(
    queue.queue
)