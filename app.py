import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from settings import load_data, save_data, set_logo_url, select_language
from display import show_products

# ---------------- CONFIG ----------------
st.set_page_config(page_title="asankar Product Preview", layout="wide")

# ---------------- LOAD SETTINGS ----------------
data = load_data()
logo_url = set_logo_url(data)
if logo_url:
    st.sidebar.image(logo_url, use_column_width=True)
language = select_language(data)

# ---------------- SIDEBAR MENU ----------------
st.sidebar.header("Menu")
menu = st.sidebar.radio("", ["Products", "Settings", "About"])

# ---------------- GOOGLE SHEET AUTH ----------------
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
    sh = gc.open(SHEET_NAME)
    worksheet = sh.sheet1
    sheet_data = worksheet.get_all_records()
    df = pd.DataFrame(sheet_data)
except Exception as e:
    st.error("❌ Failed to load Google Sheet")
    st.code(str(e))
    st.stop()

# ---------------- ROUTING ----------------
if menu == "Products":
    st.title("🖼️ Products Preview")
    tag_search = st.sidebar.text_input("Search Tag (any language)")
    media_type = st.sidebar.selectbox("Media Type", ["All", "Images", "Videos"])
    show_products(df.to_dict("records"), media_type, tag_search)

elif menu == "Settings":
    st.title("⚙️ Settings")
    st.write("Change your app settings here.")
    # Only logo and language are here, no products

elif menu == "About":
    st.title("ℹ️ About")
    st.write("asankar Product Preview App.\nManage products, preview images/videos, and configure settings.")
