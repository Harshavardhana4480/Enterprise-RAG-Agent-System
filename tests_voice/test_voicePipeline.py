from src.voice.voice_pipeline import VoicePipeline

pipeline = VoicePipeline()


result = pipeline.process_audio(
    "voice-sample.wav"
)


print("\n------------------------------")
print("VOICE PIPELINE RESULT")
print("------------------------------")

print("\nUser:")
print(result["question"])

print("\nAgent:")
print(result["answer"])

print("\nAudio:")
print(result["audio_path"])

print("\nLatency:")

print(
    f"STT   : {result['latency']['stt']} seconds"
)

print(
    f"RAG   : {result['latency']['rag']} seconds"
)

print(
    f"TTS   : {result['latency']['tts']} seconds"
)

print(
    f"Total : {result['latency']['total']} seconds"
)