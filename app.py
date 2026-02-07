import streamlit as st
from settings import load_google_sheet, sidebar_controls
from display import display_products

# Add this near the top of app.py (after page config)
add_rotated_background_logo(
    logo_path="background_logo.png",
    rotation=-25,
    opacity=0.05,
    size="300px"
)

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ----------------- Sidebar -----------------
language = sidebar_controls()

# Columns selector
columns_count = st.sidebar.slider(
    "View Columns",
    min_value=1,
    max_value=4,
    value=2
)

# Search filter
tag_search = st.sidebar.text_input("Search tags")

# ----------------- Load Google Sheet -----------------
df = load_google_sheet()

# Apply search filter
if tag_search:
    df = df[df.apply(lambda r: tag_search.lower() in " ".join(r.astype(str)).lower(), axis=1)]

# Lazy loading
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
