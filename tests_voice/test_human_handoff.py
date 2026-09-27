from src.voice.voice_pipeline import VoicePipeline

pipeline = VoicePipeline()


session_id = pipeline.create_session()


result = pipeline.process_handoff(
    session_id=session_id,
    question=(
        "I want to speak to a human."
    ),
    reason="USER_REQUEST"
)


print("\n==============================")
print("HUMAN HANDOFF")
print("==============================")


print("\nAnswer:")
print(result["answer"])


print("\nRoute:")
print(result["route"])


print("\nHandoff Payload:")
print(result["handoff"])