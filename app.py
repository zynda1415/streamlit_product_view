import streamlit as st
import pandas as pd
import gspread
import hashlib
import json

from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh

from settings import sidebar_logo
from display import display_products

# ---------- PAGE ----------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ---------- AUTO REFRESH (1 HOUR) ----------
st_autorefresh(
    interval=3600000,   # 1 hour
    key="hourly_refresh"
)

# ---------- SIDEBAR ----------
sidebar_logo()

st.sidebar.markdown("### View")
columns = st.sidebar.slider(
    "Columns",
    min_value=1,
    max_value=5,
    value=2
)

if st.sidebar.button("🔄 Refresh now"):
    st.rerun()

# ---------- GOOGLE SHEETS AUTH ----------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)

# ---------- LOAD + CHANGE DETECTION ----------
def sheet_signature(records):
    raw = json.dumps(records, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()

def load_sheet():
    sh = gc.open("asankar_product_images")  # ✔ correct name
    ws = sh.sheet1
    records = ws.get_all_records()
    sig = sheet_signature(records)
    return records, sig

records, sig = load_sheet()

if "sheet_sig" not in st.session_state:
    st.session_state.sheet_sig = sig
elif st.session_state.sheet_sig != sig:
    st.session_state.sheet_sig = sig
    st.toast("📄 Google Sheet updated")

df = pd.DataFrame(records)

# ---------- VALIDATION ----------
if "URL" not in df.columns:
    st.error("Google Sheet must contain a 'URL' column")
    st.stop()

# ---------- MOBILE OPTIMIZATION ----------
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------- DISPLAY ----------
st.markdown("## 📦 Products")
display_products(df, columns)
