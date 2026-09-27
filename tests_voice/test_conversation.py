from src.agents.memory import MemoryAgent

memory = MemoryAgent()


memory.add_message(
    "What is the leave policy?",
    "The company provides annual leave."
)


memory.add_message(
    "What about sick leave?",
    "Sick leave is provided according to company policy."
)


print("\nFull history:")
print(
    memory.get_history()
)


print("\nRecent history:")
print(
    memory.get_recent_history(1)
)