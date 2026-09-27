from src.voice.audio_player import play_audio
from src.voice.audio_recorder import record_audio
from src.voice.voice_pipeline import VoicePipeline

pipeline = VoicePipeline()


session_id = pipeline.create_session()


print("\n==============================")
print("VOICE SESSION")
print("==============================")


# ------------------------------------------
# Turn 1
# ------------------------------------------

print("\nTurn 1")
print("Speak your first question...")


audio_path = record_audio(
    duration=5,
    output_path="data/audio/turn_1.wav"
)


result = pipeline.process_audio(
    audio_path,
    session_id
)


print("\nUser:")
print(result["question"])


print("\nAgent:")
print(result["answer"])


play_audio(
    result["audio_path"]
)


# ------------------------------------------
# Turn 2
# ------------------------------------------

print("\nTurn 2")
print("Speak your follow-up question...")


audio_path = record_audio(
    duration=5,
    output_path="data/audio/turn_2.wav"
)


result = pipeline.process_audio(
    audio_path,
    session_id
)


print("\nUser:")
print(result["question"])


print("\nAgent:")
print(result["answer"])


play_audio(
    result["audio_path"]
)