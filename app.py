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
st_autorefresh(interval=300000, key="5 minitus_refresh")

# ---------- SIDEBAR ----------
sidebar_logo()

language = st.sidebar.radio(
    "Language",
    ["Kurdish", "Arabic"],
    horizontal=True
)

columns = st.sidebar.slider(
    "View columns",
    min_value=1,
    max_value=4,
    value=2
)

tag_search = st.sidebar.text_input("Search tags")

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
required_cols = [
    "URL",
    "Kurdish Tags", "Kurdish Color Tags", "Kurdish Material Tags",
    "Arabic Tags", "Arabic Colors Tags", "Arabic Material Tags"
]

for c in required_cols:
    if c not in df.columns:
        st.error(f"Missing column: {c}")
        st.stop()

# ---------- TAG FILTER ----------
if tag_search:
    df = df[df.apply(
        lambda r: tag_search.lower() in " ".join(r.astype(str)).lower(),
        axis=1
    )]

# ---------- LAZY LOAD ----------
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 12

st.markdown("## 📦 Products")

masonry_grid(
    df,
    columns=columns,
    visible_count=st.session_state.visible_count,
    language=language
)

if st.session_state.visible_count < len(df):
    if st.button("⬇ Load more"):
        st.session_state.visible_count += 12
        st.rerun()

# ---------- MOBILE ----------
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)
