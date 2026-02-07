import streamlit as st
import os

def add_rotated_background_logo(
    logo_path="background_logo.png",
    rotation=-30,
    opacity=0.05,
    size="200px"
):
    """
    Safely adds a rotated logo in the background.
    - rotation: degrees (negative = counter-clockwise)
    - opacity: 0 to 1
    - size: width of the logo
    """
    if not os.path.exists(logo_path):
        st.warning(f"Background logo not found: {logo_path}")
        return

    abs_path = os.path.abspath(logo_path)
    st.markdown(f"""
    <style>
    .rotated-logo {{
        position: fixed;
        top: 50%;
        left: 50%;
        width: {size};
        height: auto;
        transform: translate(-50%, -50%) rotate({rotation}deg);
        opacity: {opacity};
        z-index: 0;
        pointer-events: none;
    }}
    .stApp {{
        position: relative;
        z-index: 1;
    }}
    </style>
    <img src="file://{abs_path}" class="rotated-logo">
    """, unsafe_allow_html=True)
