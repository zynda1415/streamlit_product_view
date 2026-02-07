import streamlit as st
from settings import load_data, admin_login, admin_settings
from display import show_header

st.set_page_config(
    page_title="Product Viewer",
    layout="wide",
    initial_sidebar_state="collapsed"  # mobile friendly
)

data = load_data()

# Header
show_header(data.get("logo_url"))

# Admin-only sidebar
if admin_login():
    admin_settings(data)

# Main content
st.markdown("## 🛒 Products")
st.write("Products are loaded from Google Sheets.")
