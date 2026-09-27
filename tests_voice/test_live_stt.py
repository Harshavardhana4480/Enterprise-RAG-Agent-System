from src.voice.audio_recorder import record_audio
from src.voice.speech_to_text import transcribe_audio

audio_path = record_audio(
    duration=5
)


text = transcribe_audio(
    audio_path
)


print("\n------------------------------")
print("LIVE STT RESULT")
print("------------------------------")

print("\nTranscription:")
print(text)