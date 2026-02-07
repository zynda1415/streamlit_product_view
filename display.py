import streamlit as st
import re

# ---------- HEADER ----------
def show_header(data):
    col1, col2 = st.columns([1, 5])

    with col1:
        if data.get("logo_url"):
            st.image(data["logo_url"], use_container_width=True)

    with col2:
        st.markdown("## 🛍️ Asankar Product Gallery")

# ---------- YOUTUBE ID ----------
def extract_youtube_id(url):
    match = re.search(r"(?:v=|youtu.be/)([^&?/]+)", url)
    return match.group(1) if match else None

# ---------- PRODUCTS ----------
def show_products(df, data):
    st.markdown("### 📦 Products")

    if df.empty:
        st.info("No products to display")
        return

    cols = st.columns(2)  # mobile friendly

    for i, row in df.iterrows():
        col = cols[i % 2]
        url = str(row.get("URL", "")).strip().lower()

        with col:
            # IMAGE
            if url.endswith((".jpg", ".jpeg", ".png", ".webp")):
                st.image(url, use_container_width=True)

            # YOUTUBE
            elif "youtu" in url:
                vid = extract_youtube_id(url)
                if vid:
                    st.video(f"https://www.youtube.com/watch?v={vid}")

            else:
                st.warning("Unsupported media")

            # TAGS
            if data["language"] == "Kurdish":
                st.caption(row.get("Kurdish Tags", ""))
            else:
                st.caption(row.get("Arabic Tags", ""))
