from src.voice.audio_player import play_audio
from src.voice.audio_recorder import record_audio
from src.voice.voice_pipeline import VoicePipeline

print("\n==============================")
print("VOICE AGENT")
print("==============================")

print(
    "\nPlease speak after recording starts..."
)


audio_path = record_audio(
    duration=5
)


pipeline = VoicePipeline()


result = pipeline.process_audio(
    audio_path
)


print("\n------------------------------")
print("USER")
print("------------------------------")

print(result["question"])


print("\n------------------------------")
print("AGENT")
print("------------------------------")

print(result["answer"])


print("\n------------------------------")
print("LATENCY")
print("------------------------------")

print(
    f"STT   : "
    f"{result['latency']['stt']} seconds"
)

print(
    f"RAG   : "
    f"{result['latency']['rag']} seconds"
)

print(
    f"TTS   : "
    f"{result['latency']['tts']} seconds"
)

print(
    f"Total : "
    f"{result['latency']['total']} seconds"
)


print("\nPlaying response...")


play_audio(
    result["audio_path"]
)


print("\nVoice interaction completed.")