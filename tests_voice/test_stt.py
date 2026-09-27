from src.voice.speech_to_text import transcribe_audio

audio_file = r"D:\Live Projects\Enterprise RAG Agent System\voice-sample.wav"

text = transcribe_audio(audio_file);

print("\n  Transcribed text: ", text) 
#(We need to test this for Speect to text now it is pending due to not available of credits)