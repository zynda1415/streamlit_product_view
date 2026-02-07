import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

# ---------------- LOGO ----------------
def show_logo(logo_url: str | None = None, in_sidebar=False):
    """Show fallback logo at top of sidebar or page"""
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
    if in_sidebar:
        st.sidebar.markdown("<h3 style='text-align:center'>ASANKAR</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center'>ASANKAR</h2>", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def is_youtube(url: str):
    return "youtube.com" in url or "youtu.be" in url

def is_image(url: str):
    return any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"])

def clear_preview():
    st.session_state.preview_url = None

# ---------------- PRODUCT DISPLAY ----------------
def display_products(products, num_columns=3):
    """
    Pinterest-style grid with click-to-preview
    """
    if "preview_url" not in st.session_state:
        st.session_state.preview_url = None

    if not products:
        st.info("No products to display")
        return

    for i in range(0, len(products), num_columns):
        row = products[i:i + num_columns]
        cols = st.columns(num_columns, gap="medium")
        for j, (col, product) in enumerate(zip(cols, row)):
            with col:
                display_single_product(product, key_suffix=f"{i+j}")

    # Modal preview
    if st.session_state.preview_url:
        st.markdown("---")
        st.subheader("🔍 Preview")
        url = st.session_state.preview_url
        if is_youtube(url):
            st.video(url)
        elif is_image(url):
            st.image(url, use_container_width=True)
        st.button("Close Preview", on_click=clear_preview, key="close_preview")

def display_single_product(product, key_suffix=""):
    """Show one product thumbnail + title with unique keys"""
    title = product.get("title", "")
    media = product.get("media", "")

    if is_youtube(media):
        st.video(media, start_time=0)
    elif is_image(media):
        # Unique key for button
        if st.button(f"🔍 {title}", key=f"{media}_{key_suffix}"):
            st.session_state.preview_url = media
        st.image(media, use_container_width=True)
    else:
        st.warning("Unsupported media type")

    st.markdown(f"<p style='text-align:center'>{title}</p>", unsafe_allow_html=True)
