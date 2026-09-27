from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from loguru import logger

from src.agents.orchestrator import AgentOrchestrator
from src.chunking.chunk_manager import generate_chunks
from src.embeddings.embedding_service import create_embedding
from src.ingestion.document_cleaner import clean_text
from src.ingestion.document_loader import load_document
from src.security.input_guard import validate_user_query
from src.security.prompt_guard import detect_prompt_injection
from src.security.rate_limiter import RateLimiter
from src.services.file_service import upload_files
from src.ui.chat import chat_interface
from src.ui.sidebar import render_sidebar
from src.ui.uploader import upload_documents
from src.vectorstore.vector_service import store_chunks
from src.voice.input_normalizer import normalize_voice_input
from src.voice.speech_to_text import transcribe_audio
from src.voice.text_to_speech import generate_speech
from src.voice.intent_classifier import classify_intent


# --------------------------------------------------
# Environment and Logging Configuration
# --------------------------------------------------

load_dotenv()

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "application.log",
    level="INFO",
    rotation="10 MB",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} - "
        "{message}"
    ),
)


# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise RAG Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# Voice Mode Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .voice-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .voice-header h1 {
        font-size: 42px;
        margin-bottom: 4px;
    }

    .voice-header p {
        font-size: 17px;
        opacity: 0.70;
    }

    .voice-card {
        max-width: 700px;
        margin: 28px auto 24px auto;
        padding: 42px 30px;
        border-radius: 28px;
        text-align: center;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.10);
    }

    .voice-icon {
        font-size: 72px;
        line-height: 1;
        margin-bottom: 18px;
    }

    .voice-status {
        font-size: 25px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .voice-subtitle {
        font-size: 16px;
        opacity: 0.65;
    }

    .voice-user {
        padding: 16px 20px;
        border-radius: 16px;
        margin-top: 18px;
        background: rgba(30, 100, 180, 0.18);
    }

    .voice-assistant {
        padding: 20px;
        border-radius: 16px;
        margin-top: 12px;
        background: rgba(255, 255, 255, 0.055);
    }

    .conversation-title {
        margin-top: 30px;
        margin-bottom: 10px;
        font-size: 21px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Application Services
# --------------------------------------------------

orchestrator = AgentOrchestrator()
limiter = RateLimiter()

if "processed_files" not in st.session_state:
    st.session_state["processed_files"] = set()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "voice_mode" not in st.session_state:
    st.session_state.voice_mode = False


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("Enterprise RAG Agent")

st.markdown(
    """
    Upload your documents and ask questions regarding their content.
    """
)


# --------------------------------------------------
# Sidebar Configuration
# --------------------------------------------------

selected_model = render_sidebar()

st.write(f"Current model: {selected_model}")


# --------------------------------------------------
# Document Upload Section
# --------------------------------------------------

selected_files = upload_documents()

if selected_files:

    files_to_process = [
        file
        for file in selected_files
        if file.name not in st.session_state.processed_files
    ]

    if files_to_process:

        try:

            logger.info(
                f"Received {len(files_to_process)} new file(s) "
                "for upload."
            )

            uploaded_files = upload_files(files_to_process)

            if uploaded_files:

                for file_path in uploaded_files:

                    logger.info(
                        f"Starting document processing: "
                        f"{file_path.name}"
                    )

                    # Step 1: Load document
                    logger.info("STEP 1: Starting document loading")

                    raw_text = load_document(file_path)

                    logger.info(
                        f"STEP 1 COMPLETE: Document loaded "
                        f"({len(raw_text)} characters)"
                    )


                    # Step 2: Clean document
                    logger.info("STEP 2: Starting text cleaning")

                    cleaned_text = clean_text(raw_text)

                    logger.info(
                        f"STEP 2 COMPLETE: Text cleaned "
                        f"({len(cleaned_text)} characters)"
                    )


                    # Step 3: Generate chunks
                    logger.info("STEP 3: Starting chunk generation")

                    chunk_objects = generate_chunks(
                        cleaned_text,
                        file_path.name
                    )

                    logger.info(
                        f"STEP 3 COMPLETE: Generated "
                        f"{len(chunk_objects)} chunks"
                    )


                    # Step 4: Extract chunk text
                    logger.info("STEP 4: Extracting chunk text")

                    chunk_texts = [
                        chunk["text"]
                        for chunk in chunk_objects
                    ]

                    logger.info(
                        f"STEP 4 COMPLETE: Extracted "
                        f"{len(chunk_texts)} chunk texts"
                    )


                    # Step 5: Create embeddings
                    logger.info("STEP 5: Starting embedding generation")

                    embeddings = create_embedding(
                        chunk_texts
                    )

                    logger.info(
                        f"STEP 5 COMPLETE: Generated "
                        f"{len(embeddings)} embeddings"
                    )


                    # Step 6: Store vectors
                    logger.info("STEP 6: Starting ChromaDB storage")

                    store_chunks(
                        chunk_objects,
                        embeddings
                    )

                    logger.info("STEP 6 COMPLETE: ChromaDB storage finished")

                    st.session_state.processed_files.add(
                        file_path.name
                    )

                st.success(
                    f"{len(uploaded_files)} file(s) "
                    "uploaded and processed successfully."
                )

        except ValueError as error:

            logger.warning(
                f"File processing error: {error}"
            )

            st.warning(str(error))

        except Exception as error:

            logger.exception(error)

            st.error(
                "Unable to upload and process the document."
            )

    else:

        st.info(
            "The selected file has already been "
            "uploaded and processed."
        )


# --------------------------------------------------
# Normal Chat Mode
# --------------------------------------------------

if not st.session_state.voice_mode:

    question = chat_interface()

    st.divider()

    if st.button(
        "🎙️ Start Voice Mode",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.voice_mode = True
        st.rerun()


# --------------------------------------------------
# Voice Mode
# --------------------------------------------------

if st.session_state.voice_mode:

    st.markdown(
        """
        <div class="voice-header">
            <h1>🎙️ Voice Mode</h1>
            <p>Talk naturally with Jarvis</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "↩️ Exit Voice Mode",
        use_container_width=True,
    ):

        st.session_state.voice_mode = False
        st.rerun()

    st.markdown(
        """
        <div class="voice-card">
            <div class="voice-icon">🎙️</div>
            <div class="voice-status">Ready to Listen</div>
            <div class="voice-subtitle">
                Click the microphone below and speak to Jarvis
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    intent_result = None

    audio_input = st.audio_input(
        "🎙️ Speak to Jarvis",
        key="voice_input",
    )

    question = None

    if audio_input is not None:

        try:

            AUDIO_DIR = Path("data/audio")
            AUDIO_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            input_audio_path = (
                AUDIO_DIR / "mic_input.wav"
            )

            with open(
                input_audio_path,
                "wb",
            ) as audio_file:

                audio_file.write(
                    audio_input.getbuffer()
                )

            logger.info(
                f"Microphone recording saved to: "
                f"{input_audio_path}"
            )

            voice_question = transcribe_audio(
                input_audio_path
            )

            voice_question = normalize_voice_input(
                voice_question
            )

            if voice_question:

                intent_result = classify_intent(
                    voice_question
                )

                logger.info(
                    f"Detected voice intent: {intent_result}"
                )

                logger.info(
                    f"Routing voice request with intent: "
                    f"{intent_result['intent']}"
                )

                question = voice_question

                st.markdown(
                    '<div class="conversation-title">'
                    '💬 Conversation'
                    '</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"""
                    <div class="voice-user">
                        <strong>🧑 You</strong><br><br>
                        {question}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.warning(
                    "I could not understand the audio. "
                    "Please try speaking again."
                )

        except ValueError as error:

            logger.warning(
                f"Voice input validation error: {error}"
            )

            st.warning(str(error))

        except Exception as error:

            logger.exception(
                f"Voice input processing failed: {error}"
            )

            st.error(
                "Unable to process microphone input. "
                "Please try again."
            )


# --------------------------------------------------
# Voice Request Processing
# --------------------------------------------------

if (
    st.session_state.voice_mode
    and question
    and intent_result is not None
):

    detected_intent = intent_result["intent"]

    # --------------------------------------------------
    # Greeting
    # --------------------------------------------------

    if detected_intent == "GREETING":

        answer = (
            "Hello! Good morning. "
            "How can I help you today?"
        )

        logger.info(
            "Greeting intent detected. Skipping RAG."
        )

        try:

            audio_path = generate_speech(answer)

            logger.info(
                f"TTS audio generated: {audio_path}"
            )

            st.markdown(
                f"""
                <div class="voice-assistant">
                    <strong>🤖 Jarvis</strong><br><br>
                    {answer}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.audio(
                audio_path,
                format="audio/mp3",
                autoplay=True,
            )

            st.session_state.chat_history.append(
                {
                    "Question": question,
                    "Answer": answer,
                }
            )

        except Exception as error:

            logger.exception(
                f"Greeting TTS failed: {error}"
            )

            st.error(
                "Unable to generate voice response."
            )

    # --------------------------------------------------
    # Goodbye
    # --------------------------------------------------

    elif detected_intent == "GOODBYE":

        answer = "Goodbye! Have a great day."

        logger.info(
            "Goodbye intent detected. Skipping RAG."
        )

        try:

            audio_path = generate_speech(answer)

            logger.info(
                f"TTS audio generated: {audio_path}"
            )

            st.markdown(
                f"""
                <div class="voice-assistant">
                    <strong>🤖 Jarvis</strong><br><br>
                    {answer}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.audio(
                audio_path,
                format="audio/mp3",
                autoplay=True,
            )

            st.session_state.chat_history.append(
                {
                    "Question": question,
                    "Answer": answer,
                }
            )

        except Exception as error:

            logger.exception(
                f"Goodbye TTS failed: {error}"
            )

            st.error(
                "Unable to generate voice response."
            )

    # --------------------------------------------------
    # Other Intents → RAG
    # --------------------------------------------------

    else:

        is_valid, message = validate_user_query(question)

        if not is_valid:

            logger.warning(
                f"Invalid user query: {message}"
            )

            st.warning(message)

        elif not limiter.allow():

            logger.warning("Rate limit exceeded.")

            st.warning(
                "Too many requests. "
                "Please wait a few seconds."
            )

        elif not detect_prompt_injection(question):

            logger.warning(
                "Potential prompt injection attempt detected."
            )

            st.warning(
                "Potential prompt injection detected."
            )

        else:

            try:

                with st.spinner(
                    "🤔 Jarvis is thinking..."
                ):

                    answer = orchestrator.execute(question)

                st.markdown(
                    f"""
                    <div class="voice-assistant">
                        <strong>🤖 Jarvis</strong><br><br>
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                audio_path = generate_speech(answer)

                logger.info(
                    f"TTS audio generated: {audio_path}"
                )

                st.audio(
                    audio_path,
                    format="audio/mp3",
                    autoplay=True,
                )

                st.session_state.chat_history.append(
                    {
                        "Question": question,
                        "Answer": answer,
                    }
                )

            except ValueError as error:

                logger.warning(
                    f"RAG validation error: {error}"
                )

                st.warning(str(error))

            except Exception:

                logger.exception(
                    "RAG request processing failed."
                )

                st.error(
                    "Unable to process your question. "
                    "Please try again."
                )


# --------------------------------------------------
# Normal Text Chat → RAG
# --------------------------------------------------

if not st.session_state.voice_mode and question:

    is_valid, message = validate_user_query(question)

    if not is_valid:

        logger.warning(
            f"Invalid user query: {message}"
        )

        st.warning(message)

    elif not limiter.allow():

        logger.warning("Rate limit exceeded.")

        st.warning(
            "Too many requests. "
            "Please wait a few seconds."
        )

    elif not detect_prompt_injection(question):

        logger.warning(
            "Potential prompt injection attempt detected."
        )

        st.warning(
            "Potential prompt injection detected."
        )

    else:

        try:

            with st.spinner(
                "Your query is being processed. "
                "Please wait..."
            ):

                answer = orchestrator.execute(question)

            st.info(
                f"**Your Query:** {question}"
            )

            st.write(answer)

            st.session_state.chat_history.append(
                {
                    "Question": question,
                    "Answer": answer,
                }
            )

        except ValueError as error:

            logger.warning(
                f"RAG validation error: {error}"
            )

            st.warning(str(error))

        except Exception:

            logger.exception(
                "RAG request processing failed."
            )

            st.error(
                "Unable to process your question. "
                "Please try again."
            )


# --------------------------------------------------
# Voice Conversation History
# --------------------------------------------------

if st.session_state.voice_mode:

    if st.session_state.chat_history:

        st.markdown(
            '<div class="conversation-title">'
            '🗣️ Conversation History'
            '</div>',
            unsafe_allow_html=True,
        )

        for item in st.session_state.chat_history:

            st.markdown(
                f"""
                <div class="voice-user">
                    <strong>🧑 You</strong><br><br>
                    {item["Question"]}
                </div>

                <div class="voice-assistant">
                    <strong>🤖 Jarvis</strong><br><br>
                    {item["Answer"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


# --------------------------------------------------
# Normal Chat History
# --------------------------------------------------

if not st.session_state.voice_mode:

    if st.session_state.chat_history:

        st.subheader("Chat History")

        for item in st.session_state.chat_history:

            st.write(
                f"**Question:** {item['Question']}"
            )

            st.write(
                f"**Answer:** {item['Answer']}"
            )


# --------------------------------------------------
# Reset Chat
# --------------------------------------------------

if st.button(
    "Reset Chat",
    use_container_width=True,
):

    st.session_state.chat_history = []
    st.session_state.voice_mode = False
    st.rerun()
