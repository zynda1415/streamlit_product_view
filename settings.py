import streamlit as st
import json
import os

DATA_FILE = "app_data.json"
ADMIN_PASSWORD = "1234"   # change later

DEFAULT_DATA = {
    "logo_url": "",
    "language": "Kurdish"
}

# ---------- DATA ----------
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

# ---------- ADMIN ----------
def admin_login():
    if "admin_logged" not in st.session_state:
        st.session_state.admin_logged = False

    st.sidebar.markdown("### 🔐 Admin Login")

    pwd = st.sidebar.text_input(
        "Password",
        type="password",
        key="admin_pwd"
    )

    if pwd == ADMIN_PASSWORD:
        st.session_state.admin_logged = True
    elif pwd:
        st.sidebar.error("Wrong password")

    return st.session_state.admin_logged

def admin_settings(data):
    st.sidebar.markdown("### ⚙️ Admin Settings")

    logo = st.sidebar.text_input(
        "Logo URL",
        value=data.get("logo_url", ""),
        key="logo_setting"
    )

    language = st.sidebar.selectbox(
        "Language",
        ["Kurdish", "Arabic"],
        index=0 if data.get("language") == "Kurdish" else 1,
        key="language_setting"
    )

    if logo != data["logo_url"] or language != data["language"]:
        data["logo_url"] = logo
        data["language"] = language
        save_data(data)
