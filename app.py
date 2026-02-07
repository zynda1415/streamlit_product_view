import streamlit as st
from settings import sidebar_logo
from display import display_products

st.set_page_config(
    page_title="Asankar Product Viewer",
    layout="wide"
)

# ---------------- MOBILE OPTIMIZATION ----------------
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
sidebar_logo()

# ---------------- VIEW SELECTOR ----------------
st.sidebar.subheader("Grid Columns (Pinterest view)")
num_columns = st.sidebar.slider(
    "Select number of columns",
    min_value=1,
    max_value=6,
    value=3,
    step=1
)

# ---------------- HEADER ----------------
st.markdown("---")
st.subheader("📦 Products")

# Example products (replace with Google Sheet)
products = [
    {"title": "Solar Panel Cleaning", "media": "https://youtu.be/EIscMS9KW8k"},
    {"title": "Before & After", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"},
    {"title": "Product 3", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"},
    {"title": "Product 4", "media": "https://youtu.be/EIscMS9KW8k"},
    {"title": "Product 5", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"},
    {"title": "Product 6", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"},
    {"title": "Product 7", "media": "https://youtu.be/EIscMS9KW8k"}
]

display_products(products, num_columns=num_columns)
