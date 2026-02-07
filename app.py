import streamlit as st
from settings import load_data, sidebar_logo_and_language
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

# ---------------- LOAD SETTINGS ----------------
data = load_data()

# ---------------- SIDEBAR ----------------
logo_url, language = sidebar_logo_and_language(data)

# ---------------- HEADER ----------------
st.markdown("---")
st.subheader("📦 Products")

# Example placeholder products (replace with Google Sheet)
products = [
    {"title": "Solar Panel Cleaning", "media": "https://youtu.be/EIscMS9KW8k"},
    {"title": "Before & After", "media": "https://i.ytimg.com/vi/0kJHbvrTx64/hq720.jpg"}
]

display_products(products)
