import streamlit as st
from iapps.diagnostic.chat_app import render_chat

st.set_page_config(
    page_title="ThinkIA — Diagnostic Médical",
    page_icon="🧠",
    layout="centered",
)

render_chat()
