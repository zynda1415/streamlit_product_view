import streamlit as st
from PIL import Image
import os
import html

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

# ---------- TRUE PINTEREST MASONRY ----------
def masonry_grid(df, columns: int, visible_count: int):
    st.markdown(f"""
    <style>
    .masonry {{
        column-count: {columns};
        column-gap: 1rem;
    }}
    .card {{
        break-inside: avoid;
        margin-bottom: 1rem;
        border-radius: 12px;
        overflow: hidden;
        background: #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .card img {{
        width: 100%;
        display: block;
    }}
    .card-title {{
        padding: 0.5rem;
        font-size: 0.85rem;
        text-align: center;
        color: #444;
    }}
    @media (max-width: 768px) {{
        .masonry {{ column-count: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='masonry'>", unsafe_allow_html=True)

    for i in range(min(len(df), visible_count)):
        row = df.iloc[i]
        url = row["URL"]
        title = html.escape(row.get("Title", ""))

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if is_youtube(url):
            st.video(url)
        elif is_image(url):
            st.image(url, use_container_width=True)
        else:
            st.markdown("<p style='padding:1rem'>Unsupported media</p>", unsafe_allow_html=True)

        if title:
            st.markdown(f"<div class='card-title'>{title}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
