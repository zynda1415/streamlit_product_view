import streamlit as st
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

def show_logo(logo_url: str | None = None, in_sidebar=False):
    """
    Display a logo. Always uses fallback logo.
    """
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

# ---------------- PRODUCT DISPLAY ----------------
def display_products(products, view: str = "medium"):
    """
    Display products with selectable view:
    extra_large / large / medium / small / list
    """
    if not products:
        st.info("No products to display")
        return

    # Columns per view
    view_columns = {
        "extra_large": 1,
        "large": 2,
        "medium": 3,
        "small": 4,
        "list": 1
    }

    cols_count = view_columns.get(view, 3)

    # List view: vertical full width
    if view == "list":
        for p in products:
            display_single_product(p, full_width=True)
    else:
        # Grid layout
        for i in range(0, len(products), cols_count):
            row = products[i:i + cols_count]
            cols = st.columns(cols_count)
            for col, p in zip(cols, row):
                with col:
                    display_single_product(p, full_width=False)

def display_single_product(product, full_width=False):
    """Display one product"""
    title = product.get("title", "")
    media = product.get("media", "")

    # Show title
    st.markdown(f"**{title}**")

    # Show media
    if is_youtube(media):
        st.video(media)
    elif is_image(media):
        st.image(media, use_container_width=True)
    else:
        st.warning("Unsupported media type")
