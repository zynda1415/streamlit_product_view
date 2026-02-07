import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

# ---------- LOGO ----------
def show_logo(in_sidebar=False):
    if os.path.exists(FALLBACK_LOGO):
        img = Image.open(FALLBACK_LOGO)
        if in_sidebar:
            st.sidebar.image(img, use_container_width=True)
        else:
            st.image(img, use_container_width=True)

# ---------- MEDIA HELPERS ----------
def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def is_image(url: str) -> bool:
    return any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"])

# ---------- PINTEREST GRID ----------
def display_products(df, columns: int):
    if df.empty:
        st.info("No products to display")
        return

    for i in range(0, len(df), columns):
        cols = st.columns(columns, gap="medium")
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(df):
                break

            row = df.iloc[idx]
            url = row["URL"]
            key_base = f"{idx}_{url}"

            with col:
                if is_youtube(url):
                    st.video(url)
                elif is_image(url):
                    st.image(url, use_container_width=True)
                else:
                    st.warning("Unsupported media")
