import streamlit as st
import json
import os

DATA_FILE = "app_data.json"

# ---------------- JSON DATA HANDLING ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"logo_url": None, "language": "Kurdish"}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {"logo_url": None, "language": "Kurdish"}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------------- LOGO URL ----------------
def set_logo_url(data):
    st.sidebar.header("Logo URL")
    url = st.sidebar.text_input("Paste Logo URL", value=data.get("logo_url", ""))
    if url:
        data["logo_url"] = url
        save_data(data)
    return data.get("logo_url")

# ---------------- LANGUAGE SELECTION ----------------
def select_language(data):
    lang = st.sidebar.selectbox(
        "Select Language",
        ["Kurdish", "Arabic"],
        index=0 if data.get("language")=="Kurdish" else 1
    )
    data["language"] = lang
    save_data(data)
    return lang
