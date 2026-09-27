class VoiceAgentError(Exception):
    """Base exception for voice-agent errors."""


class AudioRecordingError(
    VoiceAgentError
):
    """Raised when microphone recording fails."""


class SpeechToTextError(
    VoiceAgentError
):
    """Raised when speech transcription fails."""


class TextToSpeechError(
    VoiceAgentError
):
    """Raised when speech synthesis fails."""


class VoiceTimeoutError(
    VoiceAgentError
):
    """Raised when a voice operation times out."""


class ConversationStateError(
    VoiceAgentError
):
    """Raised when the conversation state is invalid."""


class HandoffError(
    VoiceAgentError
):
    """Raised when human handoff fails."""