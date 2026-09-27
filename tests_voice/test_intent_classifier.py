from src.voice.intent_classifier import classify_intent

questions = [
    "Hello Emma",
    "What is the leave policy?",
    "What about sick leave?",
    "I want to speak to a human",
    "Goodbye",
    "Tell me something completely unrelated"
]


for question in questions:

    intent = classify_intent(
        question
    )

    print(
        f"\nQuestion: {question}"
    )

    print(
        f"Intent: {intent}"
    )