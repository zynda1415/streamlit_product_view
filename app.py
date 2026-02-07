import streamlit as st
from settings import load_google_sheet, sidebar_controls
from display import display_products

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ----------------- Rotated background logo -----------------
def add_rotated_background_logo(logo_path="background_logo.png", rotation=-30, opacity=0.05, size="200px"):
    """
    Adds a rotated logo in the background.
    """
    st.markdown(f"""
    <style>
    body {{
        position: relative;
    }}
    .rotated-logo {{
        position: fixed;
        top: 50%;
        left: 50%;
        width: {size};
        height: auto;
        transform: translate(-50%, -50%) rotate({rotation}deg);
        opacity: {opacity};
        z-index: 0;
        pointer-events: none;
    }}
    .stApp {{
        z-index: 1;
    }}
    </style>
    <img src="{logo_path}" class="rotated-logo">
    """, unsafe_allow_html=True)

# Add the background logo
add_rotated_background_logo(
    logo_path="background_logo.png",
    rotation=-25,
    opacity=0.05,
    size="300px"
)

# ----------------- Sidebar -----------------
language = sidebar_controls()

columns_count = st.sidebar.slider(
    "View Columns",
    min_value=1,
    max_value=4,
    value=2
)

tag_search = st.sidebar.text_input("Search tags")

# ----------------- Load Google Sheet -----------------
df = load_google_sheet()

# Apply search filter
if tag_search:
    df = df[df.apply(lambda r: tag_search.lower() in " ".join(r.astype(str)).lower(), axis=1)]

# ----------------- Lazy loading -----------------
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 12

st.markdown("## 📦 Products")
display_products(
    df,
    language=language,
    columns_count=columns_count,
    visible_count=st.session_state.visible_count
)

# Load more button
if st.session_state.visible_count < len(df):
    if st.button("⬇ Load more"):
        st.session_state.visible_count += 12
        st.experimental_rerun()

# Mobile adjustments
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)
