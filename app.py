import streamlit as st
import pandas as pd
import gspread
import hashlib
import json

from google.oauth2.service_account import Credentials
from streamlit_autorefresh import st_autorefresh

from settings import sidebar_logo
from display import masonry_grid

# ---------- PAGE ----------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ---------- AUTO REFRESH (1 HOUR) ----------
st_autorefresh(interval=3600000, key="hourly_refresh")

# ---------- SIDEBAR ----------
sidebar_logo()

st.sidebar.markdown("### View")
columns = st.sidebar.slider("Columns", 1, 5, 3)

st.sidebar.markdown("### Filters")
kurdish_filter = st.sidebar.text_input("Kurdish tags")
arabic_filter = st.sidebar.text_input("Arabic tags")

if st.sidebar.button("🔄 Refresh now"):
    st.rerun()

# ---------- GOOGLE SHEET ----------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)

def sheet_signature(records):
    return hashlib.md5(json.dumps(records, sort_keys=True).encode()).hexdigest()

def load_sheet():
    sh = gc.open("asankar_product_images")
    ws = sh.sheet1
    records = ws.get_all_records()
    return records, sheet_signature(records)

records, sig = load_sheet()

if st.session_state.get("sheet_sig") != sig:
    st.session_state.sheet_sig = sig
    st.toast("📄 Google Sheet updated")

df = pd.DataFrame(records)

# ---------- VALIDATION ----------
required_cols = ["URL", "Kurdish Tags", "Arabic Tags"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

# ---------- TAG FILTERS ----------
if kurdish_filter:
    df = df[df["Kurdish Tags"].str.contains(kurdish_filter, case=False, na=False)]

if arabic_filter:
    df = df[df["Arabic Tags"].str.contains(arabic_filter, case=False, na=False)]

# ---------- LAZY LOADING ----------
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 12

st.markdown("## 📦 Products")

masonry_grid(df, columns, st.session_state.visible_count)

if st.session_state.visible_count < len(df):
    if st.button("⬇ Load more"):
        st.session_state.visible_count += 12
        st.rerun()

# ---------- MOBILE OPTIMIZATION ----------
st.markdown("""
<style>
.block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)
