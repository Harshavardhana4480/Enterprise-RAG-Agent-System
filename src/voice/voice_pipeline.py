import time

from loguru import logger

from src.agents.orchestrator import AgentOrchestrator
from src.security.input_guard import validate_user_query
from src.security.prompt_guard import detect_prompt_injection
from src.security.rate_limiter import RateLimiter
from src.voice.conversation_manager import ConversationManager
from src.voice.conversation_router import ConversationRouter
from src.voice.handoff_context import HandoffContextBuilder
from src.voice.handoff_manager import HandoffManager
from src.voice.handoff_payload import HandoffPayloadBuilder
from src.voice.handoff_queue import HandoffQueue
from src.voice.input_normalizer import normalize_voice_input
from src.voice.intent_classifier import classify_intent
from src.voice.session_manager import SessionManager
from src.voice.speech_to_text import transcribe_audio
from src.voice.text_to_speech import generate_speech

MAX_CONVERSATION_TURNS = 10


class VoicePipeline:

    def __init__(self):

        self.orchestrator = AgentOrchestrator()

        self.limiter = RateLimiter()

        self.session_manager = SessionManager()

        self.conversation_manager = (
            ConversationManager()
        )

        self.router = ConversationRouter()

        self.handoff_manager = HandoffManager()

        self.handoff_context_builder = (
            HandoffContextBuilder()
        )

        self.handoff_payload_builder = (
            HandoffPayloadBuilder()
        )

        self.handoff_queue = HandoffQueue()

    def create_session(self) -> str:

        return self.session_manager.create_session()

    def process_handoff(
        self,
        session_id: str,
        question: str,
        reason: str
    ) -> dict:

        history = (
            self.conversation_manager
            .get_history()
        )

        context = (
            self.handoff_context_builder
            .build_context(
                history=history,
                current_question=question,
                reason=reason
            )
        )

        payload = (
            self.handoff_payload_builder
            .build_payload(
                session_id=session_id,
                reason=reason,
                current_question=question,
                conversation_history=(
                    context["conversation_history"]
                )
            )
        )

        self.handoff_queue.add(
            payload
        )

        self.session_manager.end_session(
            session_id
        )

        answer = (
            "I understand. "
            "I'm transferring your conversation "
            "to a human agent now."
        )

        tts_start = time.perf_counter()

        try:

            audio_response = generate_speech(
                answer
            )

            tts_latency = (
                time.perf_counter()
                - tts_start
            )

        except Exception as error:

            logger.exception(
                f"Handoff TTS failed: {error}"
            )

            audio_response = None

            tts_latency = (
                time.perf_counter()
                - tts_start
            )

        return {

            "session_id":
                session_id,

            "question":
                question,

            "answer":
                answer,

            "audio_path":
                audio_response,

            "intent":
                "REQUEST_HUMAN",

            "confidence":
                1.0,

            "route":
                "HUMAN_HANDOFF",

            "handoff":
                payload,

            "latency": {

                "tts":
                    round(
                        tts_latency,
                        3
                    )
            }
        }

    def process_audio(
        self,
        audio_file_path: str,
        session_id: str
    ) -> dict:

        pipeline_start = time.perf_counter()

        # ------------------------------------------
        # Session Validation
        # ------------------------------------------

        session = self.session_manager.get_session(
            session_id
        )

        if not session:

            raise ValueError(
                f"Invalid session: {session_id}"
            )

        # ------------------------------------------
        # Step 1: Speech-to-Text
        # ------------------------------------------

        stt_start = time.perf_counter()

        question = transcribe_audio(
            audio_file_path
        )

        stt_latency = (
            time.perf_counter()
            - stt_start
        )

        if not question:

            raise ValueError(
                "No speech was detected in the audio."
            )

        # ------------------------------------------
        # Step 2: Normalize
        # ------------------------------------------

        question = normalize_voice_input(
            question
        )

        if not question:

            raise ValueError(
                "The transcribed question is empty."
            )

        # ------------------------------------------
        # Step 3: Security
        # ------------------------------------------

        is_valid, message = validate_user_query(
            question
        )

        if not is_valid:

            raise ValueError(
                message
            )

        if not self.limiter.allow():

            raise ValueError(
                "Too many requests. "
                "Please wait a few seconds."
            )

        if not detect_prompt_injection(
            question
        ):

            raise ValueError(
                "Potential prompt injection detected."
            )

        # ------------------------------------------
        # Step 4: Intent Classification
        # ------------------------------------------

        intent_result = classify_intent(
            question
        )

        intent = intent_result.get(
            "intent",
            "UNKNOWN"
        )

        confidence = float(
            intent_result.get(
                "confidence",
                0.0
            )
        )

        # ------------------------------------------
        # Step 5: Routing
        # ------------------------------------------

        route = self.router.route(
            intent,
            confidence
        )

        logger.info(
            f"Voice request routed to: {route}"
        )

        # ------------------------------------------
        # Session Turn Limit
        # ------------------------------------------

        session = self.session_manager.get_session(
            session_id
        )

        if session["turn_count"] >= MAX_CONVERSATION_TURNS:

            return self.process_handoff(
                session_id=session_id,
                question=question,
                reason="MAX_SESSION_TURNS"
            )

        # ------------------------------------------
        # Handoff Evaluation
        # ------------------------------------------

        should_handoff, handoff_reason = (
            self.handoff_manager.should_handoff(
                intent=intent,
                failed_attempts=session[
                    "failed_attempts"
                ],
                unknown_intents=session[
                    "unknown_intents"
                ]
            )
        )

        if should_handoff:

            return self.process_handoff(
                session_id=session_id,
                question=question,
                reason=handoff_reason
            )

        # ------------------------------------------
        # Track UNKNOWN Intent
        # ------------------------------------------

        if route == "UNKNOWN":

            self.session_manager.increment_unknown_intents(
                session_id=session_id
            )

        # ------------------------------------------
        # GREETING
        # ------------------------------------------

        if route == "GREETING":

            answer = (
                "Hello! How can I help you today?"
            )

            tts_start = time.perf_counter()

            try:

                audio_response = generate_speech(
                    answer
                )

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            except Exception as error:

                logger.exception(
                    f"TTS failed: {error}"
                )

                audio_response = None

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            self.session_manager.update_turn(
                session_id
            )

            total_latency = (
                time.perf_counter()
                - pipeline_start
            )

            return {

                "session_id":
                    session_id,

                "question":
                    question,

                "answer":
                    answer,

                "audio_path":
                    audio_response,

                "intent":
                    intent,

                "confidence":
                    confidence,

                "route":
                    route,

                "latency": {

                    "stt":
                        round(
                            stt_latency,
                            3
                        ),

                    "tts":
                        round(
                            tts_latency,
                            3
                        ),

                    "total":
                        round(
                            total_latency,
                            3
                        )
                }
            }

        # ------------------------------------------
        # GOODBYE
        # ------------------------------------------

        if route == "GOODBYE":

            answer = (
                "Goodbye! Have a great day."
            )

            tts_start = time.perf_counter()

            try:

                audio_response = generate_speech(
                    answer
                )

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            except Exception as error:

                logger.exception(
                    f"TTS failed: {error}"
                )

                audio_response = None

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            self.session_manager.end_session(
                session_id
            )

            total_latency = (
                time.perf_counter()
                - pipeline_start
            )

            return {

                "session_id":
                    session_id,

                "question":
                    question,

                "answer":
                    answer,

                "audio_path":
                    audio_response,

                "intent":
                    intent,

                "confidence":
                    confidence,

                "route":
                    route,

                "latency": {

                    "stt":
                        round(
                            stt_latency,
                            3
                        ),

                    "tts":
                        round(
                            tts_latency,
                            3
                        ),

                    "total":
                        round(
                            total_latency,
                            3
                        )
                }
            }

        # ------------------------------------------
        # HUMAN HANDOFF
        # ------------------------------------------

        if route == "HUMAN_HANDOFF":

            return self.process_handoff(
                session_id=session_id,
                question=question,
                reason="REQUEST_HUMAN"
            )

        # ------------------------------------------
        # UNKNOWN
        # ------------------------------------------

        if route == "UNKNOWN":

            answer = (
                "I'm sorry, I didn't fully "
                "understand that. Could you "
                "please rephrase your question?"
            )

            tts_start = time.perf_counter()

            try:

                audio_response = generate_speech(
                    answer
                )

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            except Exception as error:

                logger.exception(
                    f"TTS failed: {error}"
                )

                audio_response = None

                tts_latency = (
                    time.perf_counter()
                    - tts_start
                )

            total_latency = (
                time.perf_counter()
                - pipeline_start
            )

            return {

                "session_id":
                    session_id,

                "question":
                    question,

                "answer":
                    answer,

                "audio_path":
                    audio_response,

                "intent":
                    intent,

                "confidence":
                    confidence,

                "route":
                    route,

                "latency": {

                    "stt":
                        round(
                            stt_latency,
                            3
                        ),

                    "tts":
                        round(
                            tts_latency,
                            3
                        ),

                    "total":
                        round(
                            total_latency,
                            3
                        )
                }
            }

        # ------------------------------------------
        # RAG / FOLLOW-UP
        # ------------------------------------------

        contextual_question = (
            self.conversation_manager
            .get_context(
                question
            )
        )

        # ------------------------------------------
        # Agentic RAG
        # ------------------------------------------

        rag_start = time.perf_counter()

        try:

            answer = self.orchestrator.execute(
                contextual_question
            )

            self.session_manager.reset_failures(
                session_id
            )

        except Exception as error:

            failed_attempts = (
                self.session_manager
                .increment_failed_attempts(
                    session_id
                )
            )

            logger.exception(
                f"Voice RAG failed: {error}"
            )

            should_handoff, handoff_reason = (
                self.handoff_manager.should_handoff(
                    intent=intent,
                    failed_attempts=failed_attempts
                )
            )

            if should_handoff:

                return self.process_handoff(
                    session_id=session_id,
                    question=question,
                    reason=handoff_reason
                )

            raise

        rag_latency = (
            time.perf_counter()
            - rag_start
        )

        # ------------------------------------------
        # Save Conversation
        # ------------------------------------------

        self.conversation_manager.add_turn(
            question,
            answer
        )

        self.session_manager.update_turn(
            session_id
        )

        # ------------------------------------------
        # Text-to-Speech
        # ------------------------------------------

        tts_start = time.perf_counter()

        try:

            audio_response = generate_speech(
                answer
            )

            tts_latency = (
                time.perf_counter()
                - tts_start
            )

        except Exception as error:

            logger.exception(
                f"TTS failed: {error}"
            )

            tts_latency = (
                time.perf_counter()
                - tts_start
            )

            audio_response = None

            total_latency = (
                time.perf_counter()
                - pipeline_start
            )

            return {

                "session_id":
                    session_id,

                "question":
                    question,

                "answer":
                    answer,

                "audio_path":
                    None,

                "intent":
                    intent,

                "confidence":
                    confidence,

                "route":
                    route,

                "warning":
                    "TTS unavailable",

                "latency": {

                    "stt":
                        round(
                            stt_latency,
                            3
                        ),

                    "rag":
                        round(
                            rag_latency,
                            3
                        ),

                    "tts":
                        round(
                            tts_latency,
                            3
                        ),

                    "total":
                        round(
                            total_latency,
                            3
                        )
                }
            }

        # ------------------------------------------
        # Total Latency
        # ------------------------------------------

        total_latency = (
            time.perf_counter()
            - pipeline_start
        )

        logger.info(
            f"Voice request completed in "
            f"{total_latency:.3f} seconds."
        )

        # ------------------------------------------
        # Return Result
        # ------------------------------------------

        return {

            "session_id":
                session_id,

            "question":
                question,

            "answer":
                answer,

            "audio_path":
                audio_response,

            "intent":
                intent,

            "confidence":
                confidence,

            "route":
                route,

            "latency": {

                "stt":
                    round(
                        stt_latency,
                        3
                    ),

                "rag":
                    round(
                        rag_latency,
                        3
                    ),

                "tts":
                    round(
                        tts_latency,
                        3
                    ),

                "total":
                    round(
                        total_latency,
                        3
                    )
            }
        }