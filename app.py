from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from loguru import logger

from src.agents.orchestrator import AgentOrchestrator
from src.security.rate_limiter import RateLimiter
from src.security.prompt_guard import detect_prompt_injection
from src.services.file_service import upload_files
from src.ui.chat import chat_interface
from src.ui.sidebar import render_sidebar
from src.ui.uploader import upload_documents
from src.ingestion.document_loader import load_document
from src.ingestion.document_cleaner import clean_text
from src.chunking.chunk_manager import generate_chunks
from src.embeddings.embedding_service import create_embedding
from src.vectorstore.vector_service import store_chunks
from src.security.input_guard import validate_user_query


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
# Application Services
# --------------------------------------------------

orchestrator = AgentOrchestrator()
limiter = RateLimiter()

if "processed_files" not in st.session_state:
    st.session_state["processed_files"] = set()


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
# Application Header
# --------------------------------------------------

st.title("Enterprise RAG Agent")

st.markdown(
    """
    Upload your documents and ask questions regarding their content.
    """
)


# --------------------------------------------------
# Chat History Initialization
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


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

        file for file in selected_files

        if file.name
        not in st.session_state.processed_files

    ]

    if files_to_process:

        try:

            logger.info(
                f"Received {len(files_to_process)} "
                f"new file(s) for upload."
            )

            uploaded_files = upload_files(
                files_to_process
            )

            if uploaded_files:

                for file_path in uploaded_files:

                    logger.info(
                        f"Starting document processing: "
                        f"{file_path.name}"
                    )

                    # Step 1: Load document
                    raw_text = load_document(
                        file_path
                    )

                    # Step 2: Clean document
                    cleaned_text = clean_text(
                        raw_text
                    )

                    # Step 3: Generate chunks
                    chunk_objects = generate_chunks(
                        cleaned_text,
                        file_path.name
                    )

                    # Step 4: Extract chunk text
                    chunk_texts = [

                        chunk["text"]

                        for chunk in chunk_objects

                    ]

                    # Step 5: Create embeddings
                    embeddings = create_embedding(
                        chunk_texts
                    )

                    # Step 6: Store vectors
                    store_chunks(
                        chunk_objects,
                        embeddings
                    )

                    # Mark file as processed
                    st.session_state.processed_files.add(
                        file_path.name
                    )

                st.success(
                    f"{len(uploaded_files)} file(s) "
                    f"uploaded and processed successfully."
                )

        except ValueError as error:

            logger.warning(
                f"File processing error: {error}"
            )

            st.warning(
                str(error)
            )

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
# Chat Interface
# --------------------------------------------------

question = chat_interface()


# --------------------------------------------------
# Main RAG Request Processing
# --------------------------------------------------

if question:

    # Validate user input
    is_valid, message = validate_user_query(
        question
    )

    if not is_valid:

        logger.warning(
            f"Invalid user query: {message}"
        )

        st.warning(message)

    # Rate limiting
    elif not limiter.allow():

        logger.warning(
            "Rate limit exceeded."
        )

        st.warning(
            "Too many requests. Please wait a few seconds."
        )

    # Prompt injection protection
    elif not detect_prompt_injection(question):

        logger.warning(
            "Potential prompt injection attempt detected."
        )

        st.warning(
            "Potential prompt injection detected."
        )

    # Execute RAG workflow
    else:

        try:

            with st.spinner(
                "Your query is being processed. Please wait..."
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
# Chat History
# --------------------------------------------------

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
# Reset Chat History
# --------------------------------------------------

if st.button("Reset Chat"):

    st.session_state.chat_history = []

    st.rerun()