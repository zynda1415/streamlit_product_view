import streamlit as st
import uuid
from PIL import Image
import os

FALLBACK_LOGO = "fallback_logo.png"

# ----------------- Helpers -----------------
def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def is_image(url: str) -> bool:
    return any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])

# ----------------- Masonry Grid -----------------
def masonry_grid(df, language="Kurdish", columns=3, visible_count=12):
    """Display products in Pinterest-style masonry grid"""
    if df.empty:
        st.info("No products to display")
        return

    columns = max(1, columns)

    # CSS for masonry layout
    st.markdown(f"""
    <style>
    .masonry {{
        column-count: {columns};
        column-gap: 1rem;
    }}
    @media (max-width: 1024px) {{
        .masonry {{ column-count: max(1, {columns}-1); }}
    }}
    @media (max-width: 768px) {{
        .masonry {{ column-count: 2; }}
    }}
    @media (max-width: 480px) {{
        .masonry {{ column-count: 1; }}
    }}
    .card {{
        break-inside: avoid;
        margin-bottom: 1rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        background: white;
    }}
    .card img, .card iframe {{
        width: 100%;
        display: block;
    }}
    .card-content {{
        padding: 0.5rem 0.75rem;
        font-size: 14px;
        color: #444;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="masonry">', unsafe_allow_html=True)

    for _, row in df.head(visible_count).iterrows():
        key = str(uuid.uuid4())

        if language == "Kurdish":
            tags = row.get("Kurdish Tags", "")
            colors = row.get("Kurdish Color Tags", "")
            materials = row.get("Kurdish Material Tags", "")
        else:
            tags = row.get("Arabic Tags", "")
            colors = row.get("Arabic Colors Tags", "")
            materials = row.get("Arabic Material Tags", "")

        html = f'<div class="card" id="{key}">'

        url = row.get("URL", "")

        try:
            if is_youtube(url):
                if "youtu.be" in url:
                    video_id = url.split("/")[-1]
                else:
                    video_id = url.split("v=")[-1].split("&")[0]
                embed_url = f"https://www.youtube.com/embed/{video_id}"
                html += f'<iframe height="200" src="{embed_url}" frameborder="0" allowfullscreen></iframe>'
            elif is_image(url):
                html += f'<img src="{url}" loading="lazy">'
            else:
                html += "<div style='padding:1rem'>Unsupported media</div>"
        except Exception:
            html += "<div style='padding:1rem'>Error loading media</div>"

        html += f"""
            <div class="card-content">
                {tags}<br>{colors}<br>{materials}
            </div>
        </div>
        """

        st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
