import json
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

APP_DATA_FILE = "app_data.json"

# ---------- App data ----------
def load_app_data():
    """Load persisted app settings from JSON"""
    try:
        with open(APP_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"language": "Kurdish"}

def save_app_data(data):
    """Save app settings to JSON"""
    with open(APP_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- Google Sheet ----------
@st.cache_data(ttl=5)  # auto refresh every hour
def load_google_sheet():
    """Load Google Sheet as a Pandas DataFrame"""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(creds)

    # Google Sheet ID from Streamlit secrets
    sheet = client.open_by_key(st.secrets["google_sheet_id"]).sheet1

    df = pd.DataFrame(sheet.get_all_records())
    df.columns = df.columns.str.strip()  # remove any leading/trailing spaces
    return df

# ---------- Sidebar ----------
def sidebar_controls():
    """Display sidebar with fallback logo and language switch"""
    app_data = load_app_data()
    st.sidebar.image("fallback_logo.png", use_container_width=True)

    language = st.sidebar.radio(
        "Language / زمان",
        ["Kurdish", "Arabic"],
        index=0 if app_data.get("language", "Kurdish") == "Kurdish" else 1
    )

    app_data["language"] = language
    save_app_data(app_data)

    return language
