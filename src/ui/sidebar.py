import streamlit as st


def render_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.header("Project")
    st.sidebar.write("Enterprise RAG Agent")
    st.sidebar.divider()
    st.sidebar.header("Configuration")
    model=st.sidebar.selectbox("Choose Model", ["gpt-5-mini",
                                                "gpt-5-medium"])

    return model