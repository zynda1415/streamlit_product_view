import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from settings import load_data, admin_login, admin_settings
from display import show_header, show_products

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ---------------- LOAD APP DATA ----------------
data = load_data()

# ---------------- SIDEBAR ----------------
is_admin = admin_login()

if is_admin:
    admin_settings(data)

# ---------------- HEADER ----------------
show_header(data)

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
    sh = gc.open(SHEET_NAME)
    ws = sh.sheet1
    df = pd.DataFrame(ws.get_all_records())
except Exception as e:
    st.error("❌ Failed to load Google Sheet")
    st.code(str(e))
    st.stop()

# ---------------- SHOW PRODUCTS ----------------
show_products(df, data)
