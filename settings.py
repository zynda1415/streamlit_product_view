import streamlit as st
import json
import os

DATA_FILE = "app_data.json"
ADMIN_PASSWORD = "1234"   # change this

DEFAULT_DATA = {
    "logo_url": "",
    "language": "Kurdish"
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def admin_login():
    if "admin_logged" not in st.session_state:
        st.session_state.admin_logged = False

    with st.sidebar:
        st.markdown("### 🔐 Admin")
        pwd = st.text_input("Admin password", type="password")

        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_logged = True
        elif pwd:
            st.error("Wrong password")

    return st.session_state.admin_logged

def admin_settings(data):
    st.sidebar.markdown("### ⚙️ Settings")

    logo_url = st.sidebar.text_input(
        "Logo URL",
        value=data.get("logo_url", ""),
        key="admin_logo_url"
    )

    language = st.sidebar.selectbox(
        "Language",
        ["Kurdish", "Arabic"],
        index=0 if data.get("language") == "Kurdish" else 1,
        key="admin_language"
    )

    if logo_url != data["logo_url"] or language != data["language"]:
        data["logo_url"] = logo_url
        data["language"] = language
        save_data(data)
