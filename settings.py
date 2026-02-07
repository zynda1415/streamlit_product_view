import streamlit as st
import uuid

FALLBACK_LOGO = "fallback_logo.png"

# ---------- LOGO ----------
def show_logo(in_sidebar=False):
    from PIL import Image
    import os
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
    return any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])

# ---------- MASONRY GRID ----------
def masonry_grid(df, language, columns=3, visible_count=12):
    if df.empty:
        st.info("No products to display")
        return

    # Pinterest masonry CSS
    st.markdown(f"""
    <style>
    .masonry {{
        column-count: {columns};
        column-gap: 1rem;
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
    .card img {{
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

        html = f"""
        <div class="card" id="{key}">
        """

        if is_youtube(row.get("URL","")):
            html += f'<iframe width="100%" height="200" src="{row["URL"]}" frameborder="0" allowfullscreen></iframe>'
        elif is_image(row.get("URL","")):
            html += f'<img src="{row["URL"]}" loading="lazy">'
        else:
            html += "<div style='padding:1rem'>Unsupported media</div>"

        html += f"""
            <div class="card-content">
                {tags}<br>{colors}<br>{materials}
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
