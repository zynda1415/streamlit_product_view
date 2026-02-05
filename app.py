import streamlit as st
from settings import load_data, save_data, set_logo_url, select_language, add_product
from display import show_products

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Asanar Product Preview", layout="wide")

# ---------------- LOAD DATA ----------------
data = load_data()

# ---------------- SIDEBAR ----------------
logo_url = set_logo_url(data)
if logo_url:
    st.sidebar.image(logo_url, use_column_width=True)

st.sidebar.header("Menu")
menu = st.sidebar.radio("", ["Products", "Settings", "About"])

language = select_language(data)

# ---------------- ROUTING ----------------
if menu == "Products":
    st.title("🖼️ Products Preview")
    tag_search = st.sidebar.text_input("Search Tag (any language)")
    media_type = st.sidebar.selectbox("Media Type", ["All", "Images", "Videos"])
    add_product(data)  # sidebar add product form
    show_products(data.get("products", []), media_type, tag_search)

elif menu == "Settings":
    st.title("⚙️ Settings")
    st.write("Change your app settings here.")
    set_logo_url(data)
    select_language(data)

elif menu == "About":
    st.title("ℹ️ About")
    st.write("Asanar Product Preview App.\nManage products, preview images/videos, and configure settings.")
