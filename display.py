import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

def show_logo(logo_url: str | None = None, in_sidebar=False):
    """Show fallback logo"""
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

def is_youtube(url: str):
    return "youtube.com" in url or "youtu.be" in url

def is_image(url: str):
    return any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"])

# ---------------- PINTEREST GRID ----------------
def display_products(products, num_columns=3):
    """
    Pinterest-style grid:
    - num_columns: number of columns in the grid
    - clickable thumbnails open preview
    """
    if "preview_url" not in st.session_state:
        st.session_state.preview_url = None

    if not products:
        st.info("No products to display")
        return

    # Calculate number of products per row
    for i in range(0, len(products), num_columns):
        row = products[i:i + num_columns]
        cols = st.columns(num_columns, gap="medium")
        for col, product in zip(cols, row):
            with col:
                display_single_product(product)

    # Modal preview
    if st.session_state.preview_url:
        st.markdown("---")
        st.subheader("🔍 Preview")
        url = st.session_state.preview_url
        if is_youtube(url):
            st.video(url)
        elif is_image(url):
            st.image(url, use_container_width=True)
        st.button("Close Preview", on_click=lambda: clear_preview())

def clear_preview():
    st.session_state.preview_url = None

def display_single_product(product):
    """Show one product thumbnail + title"""
    title = product.get("title", "")
    media = product.get("media", "")

    if is_youtube(media):
        st.video(media, start_time=0)
    elif is_image(media):
        if st.button(f"🔍 {title}", key=media):
            st.session_state.preview_url = media
        st.image(media, use_container_width=True)
    else:
        st.warning("Unsupported media type")

    st.markdown(f"<p style='text-align:center'>{title}</p>", unsafe_allow_html=True)
