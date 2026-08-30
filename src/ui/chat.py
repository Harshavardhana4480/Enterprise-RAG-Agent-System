import streamlit as st


def chat_interface():

    question = st.chat_input(
        "Enter your query here"
    )

    return question