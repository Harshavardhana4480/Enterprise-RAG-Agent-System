from src.voice.conversation_router import ConversationRouter

router = ConversationRouter()


tests = [
    ("GREETING", 0.95),
    ("RAG_QUERY", 0.92),
    ("FOLLOW_UP", 0.88),
    ("REQUEST_HUMAN", 0.97),
    ("GOODBYE", 0.91),
    ("UNKNOWN", 0.40),
]


for intent, confidence in tests:

    route = router.route(
        intent,
        confidence
    )

    print(
        f"{intent} "
        f"({confidence}) "
        f"→ {route}"
    )