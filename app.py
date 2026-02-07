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
st.sidebar.subheader("View Options")
view_option = st.sidebar.radio(
    "Select view",
    options=["extra_large", "large", "medium", "small", "list"],
    index=2  # default medium
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
    {"title": "Product 5", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"}
]

display_products(products, view=view_option)
