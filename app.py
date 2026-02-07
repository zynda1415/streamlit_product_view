import streamlit as st
from settings import load_google_sheet, sidebar_controls
from display import masonry_grid

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ----------------- Sidebar -----------------
language = sidebar_controls()  # returns "Kurdish" or "Arabic"

# Columns selector for masonry
columns = st.sidebar.slider(
    "View Columns",
    min_value=1,
    max_value=4,
    value=2
)

# Search filter
tag_search = st.sidebar.text_input("Search tags")

# ----------------- Load Google Sheet -----------------
df = load_google_sheet()

# ----------------- Apply search filter -----------------
if tag_search:
    df = df[df.apply(lambda r: tag_search.lower() in " ".join(r.astype(str)).lower(), axis=1)]

# ----------------- Lazy loading -----------------
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 12

st.markdown("## 📦 Products")
masonry_grid(
    df,
    language=language,
    columns=columns,
    visible_count=st.session_state.visible_count
)

# Load more button
if st.session_state.visible_count < len(df):
    if st.button("⬇ Load more"):
        st.session_state.visible_count += 12
        st.experimental_rerun()  # refresh to show more

# ----------------- Mobile adjustments -----------------
st.markdown("""
<style>
@media (max-width: 768px) {{
    .block-container {{ padding: 1rem; }}
}}
</style>
""", unsafe_allow_html=True)
