import streamlit as st
import uuid

def masonry_css(columns: int):
    return f"""
    <style>
    .masonry {{
        column-count: {columns};
        column-gap: 1rem;
    }}
    @media (max-width: 768px) {{
        .masonry {{
            column-count: 2;
        }}
    }}
    @media (max-width: 480px) {{
        .masonry {{
            column-count: 1;
        }}
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
    }}
    </style>
    """

def render_products(df, language, columns):
    st.markdown(masonry_css(columns), unsafe_allow_html=True)
    st.markdown('<div class="masonry">', unsafe_allow_html=True)

    for _, row in df.iterrows():
        key = str(uuid.uuid4())

        title = row["Title KU"] if language == "ku" else row["Title AR"]
        tags = (
            row["Kurdish Tags"] if language == "ku"
            else row["Arabic Tags"]
        )

        html = f"""
        <div class="card" id="{key}">
            <img src="{row['Image URL']}" loading="lazy">
            <div class="card-content">
                <b>{title}</b><br>
                <small>{tags}</small>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
