from src.voice.handoff_manager import HandoffManager

manager = HandoffManager()


# ------------------------------------------
# User requested human
# ------------------------------------------

result = manager.should_handoff(
    intent="REQUEST_HUMAN"
)

print(
    "\nUser request:"
)

print(result)


# ------------------------------------------
# Normal RAG request
# ------------------------------------------

result = manager.should_handoff(
    intent="RAG_QUERY"
)

print(
    "\nNormal request:"
)

print(result)


# ------------------------------------------
# Repeated failures
# ------------------------------------------

result = manager.should_handoff(
    intent="RAG_QUERY",
    failed_attempts=2
)

print(
    "\nRepeated failures:"
)

print(result)


# ------------------------------------------
# Unknown intent escalation
# ------------------------------------------

result = manager.should_handoff(
    intent="UNKNOWN",
    unknown_intents=2
)

print(
    "\nRepeated unknown intents:"
)

print(result)