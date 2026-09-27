from src.voice.handoff_context import HandoffContextBuilder

builder = HandoffContextBuilder()


history = [

    {
        "question":
            "What is the leave policy?",

        "answer":
            "The company provides annual leave."
    },

    {
        "question":
            "What about sick leave?",

        "answer":
            "Sick leave is covered by company policy."
    }
]


context = builder.build_context(
    history=history,
    current_question=(
        "I want to speak to a human."
    ),
    reason="USER_REQUEST"
)


print("\nHandoff Context:")
print(context)