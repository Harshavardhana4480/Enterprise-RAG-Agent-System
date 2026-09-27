from src.voice.conversation_manager import ConversationManager

manager = ConversationManager()


manager.add_turn(
    "What is the leave policy?",
    "The company provides annual leave."
)


context = manager.get_context(
    "What about sick leave?"
)


print("\nGenerated context:")
print(context)