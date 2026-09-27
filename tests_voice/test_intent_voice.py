from src.voice.audio_player import play_audio
from src.voice.audio_recorder import record_audio
from src.voice.voice_pipeline import VoicePipeline

pipeline = VoicePipeline()

session_id = pipeline.create_session()


print("\n==============================")
print("VOICE INTENT TEST")
print("==============================")


audio_path = record_audio(
    duration=5
)


result = pipeline.process_audio(
    audio_path,
    session_id
)


print("\nUser:")
print(result["question"])


print("\nIntent:")
print(result["intent"])


print("\nConfidence:")
print(result["confidence"])


print("\nRoute:")
print(result["route"])


print("\nAnswer:")
print(result["answer"])


if result["audio_path"]:

    play_audio(
        result["audio_path"]
    )