import streamlit as st
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def render_logo(width=120):
    """Renders the circular agent logo."""
    logo_path = "frontend/assets/logo.png"
    if not os.path.exists(logo_path):
         logo_path = "frontend/assests/logo.png"
         
    img_base64 = get_base64_image(logo_path)
    
    if img_base64:
        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{img_base64}" class="logo-img" style="width: {width}px; height: {width}px;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(f'<div class="logo-container"><div class="logo-img" style="display:flex; align-items:center; justify-content:center; background:#21262d; font-size:3rem; width: {width}px; height: {width}px;">🤖</div></div>', unsafe_allow_html=True)
