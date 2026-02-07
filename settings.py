import json
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

APP_DATA_FILE = "app_data.json"

# ---------- App data ----------
def load_app_data():
    try:
        with open(APP_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"language": "Kurdish"}

def save_app_data(data):
    with open(APP_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- Google Sheet ----------
@st.cache_data(ttl=3600)  # auto refresh every hour
def load_google_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key(st.secrets["google_sheet_id"]).sheet1
    df = pd.DataFrame(sheet.get_all_records())
    df.columns = df.columns.str.strip()  # remove spaces
    return df

# ---------- Sidebar ----------
def sidebar_controls():
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
