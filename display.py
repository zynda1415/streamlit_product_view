import streamlit as st

FALLBACK_LOGO = "fallback_logo.png"

def show_logo(logo_url):
    # If URL exists, try it
    if logo_url:
        try:
            st.image(logo_url, use_container_width=True)
            return
        except Exception:
            pass

    # Always fallback safely
    st.image(FALLBACK_LOGO, use_container_width=True)


def is_youtube(url):
    return "youtube.com" in url or "youtu.be" in url

def is_image(url):
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
