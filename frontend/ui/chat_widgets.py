import streamlit as st
import os
import base64
from frontend.ui.animations import get_typing_indicator

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def render_welcome_message():
    """Renders a friendly welcome message when chat is empty."""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem; color: rgba(255,255,255,0.7);">
        <h1 style="color: #46b8c9;"> Agent Solver</h1>
        <p style="font-size: 1.2rem;">Expert STEM & Technical Assistant</p>
        <p>I help you solve complex problems and analyze technical documentation.</p>
        <br>
        <p style="font-size: 0.9rem; opacity: 0.8;">👈 <b>Upload your STEM documentation to begin</b></p>
    </div>
    """, unsafe_allow_html=True)

def render_chat(history):
    """Render chat history with modern styling."""
    # Use cached logo if available, else fallback to standard robot
    avatar_data = st.session_state.get("logo_b64", "🤖")

    for msg in history:
        avatar = avatar_data if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

def render_sources(used_excerpts):
    """Render source excerpts in a modern, collapsible format."""
    if not used_excerpts:
        return

    with st.expander(f"🔎 Cited Sources ({len(used_excerpts)})", expanded=False):
        for i, ex in enumerate(used_excerpts, start=1):
            # Simple clean card for each source
            st.markdown(f"""
            <div style="margin-bottom: 1rem; border: 1px solid #30363d; border-radius: 8px; padding: 1rem; background-color: #161b22;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="color: #46b8c9;">📄 Source {i}</strong>
                    <span style="font-size: 0.8rem; background: #30363d; padding: 0.2rem 0.5rem; border-radius: 4px; color: #a0a0a0;">
                        Match: {ex['score']:.2f}
                    </span>
                </div>
                <div style="color: #8b949e; font-size: 0.85rem; margin-bottom: 0.5rem;">
                    From: <code>{ex['doc_name']}</code>
                </div>
                <div style="font-style: italic; color: #c9d1d9; padding: 0.5rem; background: #0d1117; border-radius: 6px; border-left: 3px solid #46b8c9;">
                    "{ex["text"][:300]}..."
                </div>
            </div>
            """, unsafe_allow_html=True)
