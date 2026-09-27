from src.voice.audio_recorder import record_audio

audio_path = record_audio(
    duration=5
)


print("\nAudio recorded successfully:")
print(audio_path)