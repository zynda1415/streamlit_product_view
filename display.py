import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

def show_logo(logo_url: str | None, in_sidebar=False):
    """
    Display a logo.
    If logo_url is provided, try to load it.
    Else fallback to local image.
    """
    try:
        if logo_url:
            if in_sidebar:
                st.sidebar.image(logo_url, use_container_width=True)
            else:
                st.image(logo_url, use_container_width=True)
            return
    except Exception:
        pass

    # Fallback logo
    if os.path.exists(FALLBACK_LOGO):
        try:
            img = Image.open(FALLBACK_LOGO)
            if in_sidebar:
                st.sidebar.image(img, use_container_width=True)
            else:
                st.image(img, use_container_width=True)
            return
        except Exception:
            pass

    # Last fallback: text
    if in_sidebar:
        st.sidebar.markdown("<h3 style='text-align:center'>ASANKAR</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center'>ASANKAR</h2>", unsafe_allow_html=True)


def is_youtube(url: str):
    return "youtube.com" in url or "youtu.be" in url


def is_image(url: str):
    return any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"])


def display_products(products):
    if not products:
        st.info("No products to display")
        return

    for p in products:
        st.markdown(f"### {p.get('title', '')}")

        media = p.get("media", "")

        if is_youtube(media):
            st.video(media)
        elif is_image(media):
            st.image(media, use_container_width=True)
        else:
            st.warning("Unsupported media type")
