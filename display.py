import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

def show_logo(logo_url: str | None = None, in_sidebar=False):
    """Always use fallback logo for simplicity"""
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

# ---------------- ICON GRID ----------------
def display_products(products, view: str = "medium"):
    """
    Explorer-style display:
    extra_large / large / medium / small / list
    """
    if not products:
        st.info("No products to display")
        return

    # Thumbnail sizes per view
    thumb_sizes = {
        "extra_large": 400,
        "large": 300,
        "medium": 200,
        "small": 120,
        "list": 0  # full width
    }

    thumb_size = thumb_sizes.get(view, 200)

    # Columns per row
    cols_per_row = {
        "extra_large": 1,
        "large": 2,
        "medium": 3,
        "small": 4,
        "list": 1
    }

    cols_count = cols_per_row.get(view, 3)

    if view == "list":
        # Vertical full-width list
        for product in products:
            display_single_product(product, full_width=True)
    else:
        # Grid layout
        for i in range(0, len(products), cols_count):
            row = products[i:i + cols_count]
            cols = st.columns(cols_count, gap="medium")
            for col, product in zip(cols, row):
                with col:
                    display_single_product(product, thumb_size=thumb_size)

def display_single_product(product, thumb_size=200, full_width=False):
    """Display a single product as thumbnail + title"""
    title = product.get("title", "")
    media = product.get("media", "")

    if full_width:
        st.markdown(f"### {title}")
        if is_youtube(media):
            st.video(media)
        elif is_image(media):
            st.image(media, use_container_width=True)
        else:
            st.warning("Unsupported media type")
    else:
        # Explorer-style thumbnail
        if is_youtube(media):
            # Embed video as small player
            st.video(media)
        elif is_image(media):
            st.image(media, width=thumb_size)
        else:
            st.warning("Unsupported media type")

        st.markdown(f"<p style='text-align:center'>{title}</p>", unsafe_allow_html=True)
