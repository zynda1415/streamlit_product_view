import streamlit as st
from settings import load_data, sidebar_logo_and_language
from display import show_logo, display_products

st.set_page_config(
    page_title="Product Viewer",
    layout="wide"
)

# ---------------- MOBILE DETECTION ----------------
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
data = load_data()

# ---------------- SIDEBAR ----------------
logo_url, language = sidebar_logo_and_language(data)

# ---------------- HEADER ----------------
show_logo(logo_url)

st.markdown("---")

# ---------------- CONTENT ----------------
st.subheader("📦 Products")

# Example placeholder (replace with Google Sheet data)
products = [
    {
        "title": "Solar Panel Cleaning",
        "media": "https://youtu.be/EIscMS9KW8k"
    },
    {
        "title": "Before / After",
        "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"
    }
]

display_products(products)
