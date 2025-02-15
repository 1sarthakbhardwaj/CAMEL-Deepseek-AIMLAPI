"""
main.py

This file contains the Streamlit user interface for the DeepSeek‑R1 Q&A application
using the CAMEL framework. Users can upload a document, configure API keys,
and ask questions about the document.
"""

import os
import streamlit as st
from app import process_query

# ------------------------------------------------
# Custom CSS Styling for an improved dark UI
# ------------------------------------------------
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stChatInput input {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #3A3A3A !important;
    }
    .stFileUploader {
        border-radius: 5px;
        padding: 15px;
    }
    h1 {
        font-size: 30px !important;
    }
    h3 {
        font-size: 20px !important;
    }
    .highlight-text {
        color: #00FFAA;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# App Title and Description
# ------------------------------------------------
st.markdown(
    """
    <h1>RAG App using DEEPSEEK‑R1 & CAMEL‑AI Agent</h1>
    """,
    unsafe_allow_html=True
)
st.markdown("### Chat with your document effortlessly – no more wrong answers!")

# ------------------------------------------------
# Sidebar: API Key Configuration
# ------------------------------------------------
with st.sidebar:
    st.header("⚙ Configuration")
    openai_key = st.text_input("Enter your OpenAI API Key", type="password")
    deepseek_key = st.text_input("Enter your DeepSeek API Key", type="password")
    if openai_key and deepseek_key:
        st.success("API Keys set! ✅")
    st.markdown("---")

if not (openai_key and deepseek_key):
    st.warning("⚠ Please enter both API keys in the sidebar to continue.")
    st.stop()

# Set API keys in environment variables.
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["DEEPSEEK_API_KEY"] = deepseek_key

# ------------------------------------------------
# File Upload Section
# ------------------------------------------------
uploaded_file = st.file_uploader("Upload a document (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
file_path = None
if uploaded_file:
    os.makedirs("uploaded_files", exist_ok=True)
    file_path = os.path.join("uploaded_files", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ File '{uploaded_file.name}' uploaded and ready for analysis.")

# ------------------------------------------------
# User Query Input & AI Response Handling
# ------------------------------------------------
user_query = st.text_input("🔍 Ask a question about the document:")
if user_query:
    with st.spinner("Processing your query... 🔄"):
        answer = process_query(user_query, file_path)
    st.markdown(f"**Answer:** {answer}")
