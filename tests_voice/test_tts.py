from src.voice.text_to_speech import generate_speech

text = "Hello, this is a test for text-to-speech conversion."
audio_path = generate_speech(text)
print("\n  Generated audio file path: ", audio_path)
#(We need to test this for Text to speech now it is pending due to not available of credits)