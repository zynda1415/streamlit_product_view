import streamlit as st
import json
import os

DATA_FILE = "app_data.json"

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

def sidebar_logo_and_language(data):
    from display import FALLBACK_LOGO, show_logo  # avoid circular import

    # ---------------- LOGO ----------------
    logo_url = data.get("logo_url", "")
    show_logo(logo_url, in_sidebar=True)  # display fallback if URL empty

    # ---------------- SETTINGS ----------------
    st.sidebar.subheader("⚙️ Settings")

    # OPTIONAL logo URL override
    logo_url_input = st.sidebar.text_input(
        "Logo URL (optional)",
        value=logo_url,
        key="logo_url_unique"
    )

    language = st.sidebar.selectbox(
        "Language",
        ["Kurdish", "Arabic"],
        index=0 if data.get("language") == "Kurdish" else 1,
        key="language_unique"
    )

    if logo_url_input != data.get("logo_url") or language != data.get("language"):
        data["logo_url"] = logo_url_input
        data["language"] = language
        save_data(data)

    return logo_url_input, language
