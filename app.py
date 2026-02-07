import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from settings import load_data, sidebar_logo_and_language
from display import show_products

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ---------------- LOAD SETTINGS ----------------
data = load_data()
logo_url, language = sidebar_logo_and_language(data)

if logo_url:
    st.sidebar.image(logo_url, use_column_width=True)

# ---------------- MOBILE MODE ----------------
st.sidebar.header("View")
st.session_state.mobile_view = st.sidebar.toggle(
    "📱 Mobile friendly",
    value=True
)

# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Menu",
    ["Products", "Settings", "About"]
)

# ---------------- GOOGLE SHEETS ----------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)

SHEET_NAME = "asankar_product_images"

try:
    sheet = gc.open(SHEET_NAME).sheet1
    records = sheet.get_all_records()
except Exception as e:
    st.error("Failed to load Google Sheet")
    st.stop()

# ---------------- ROUTES ----------------
if menu == "Products":
    st.title("🖼️ Asankar Products")

    search = st.sidebar.text_input("Search tags")
    media_type = st.sidebar.selectbox(
        "Media Type",
        ["All", "Images", "Videos"]
    )

    show_products(records, media_type, search)

elif menu == "Settings":
    st.title("⚙️ Settings")
    st.info("All settings are managed from the sidebar.")

elif menu == "About":
    st.title("ℹ️ About")
    st.write("""
    **Asankar Product Viewer**

    - Mobile-first design
    - Google Sheets backend
    - Supports images & YouTube videos
    """)
