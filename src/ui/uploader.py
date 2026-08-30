import streamlit as st
def upload_documents():

    uploaded_files = st.file_uploader(
        "Upload your files",
        type=["txt", "pdf", "csv", "xlsx"],
        accept_multiple_files=True,
        key = "uploader_documents"
    )

    return uploaded_files