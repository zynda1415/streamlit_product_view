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

# ---------- MASONRY GRID ----------
def masonry_grid(df, columns, visible_count, language):
    if df.empty:
        st.info("No products to display")
        return

    cols = st.columns(columns, gap="medium")

    for i in range(min(len(df), visible_count)):
        col = cols[i % columns]
        row = df.iloc[i]
        url = row["URL"]

        with col:
            st.markdown(
                """
                <div style="
                    border-radius:12px;
                    overflow:hidden;
                    box-shadow:0 4px 12px rgba(0,0,0,0.08);
                    margin-bottom:1rem;
                ">
                """,
                unsafe_allow_html=True,
            )

            if is_youtube(url):
                st.video(url)
            elif is_image(url):
                st.image(url, use_container_width=True)
            else:
                st.warning("Unsupported media")

            # ---------- TAG DISPLAY ----------
            if language == "Kurdish":
                tags = [
                    row.get("Kurdish Tags", ""),
                    row.get("Kurdish Color Tags", ""),
                    row.get("Kurdish Material Tags", "")
                ]
            else:
                tags = [
                    row.get("Arabic Tags", ""),
                    row.get("Arabic Colors Tags", ""),
                    row.get("Arabic Material Tags", "")
                ]

            tags = [t for t in tags if t]

            if tags:
                st.markdown(
                    "<div style='padding:0.5rem;font-size:0.8rem;color:#444'>"
                    + "<br>".join(tags)
                    + "</div>",
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
