import streamlit as st
from display import show_logo
import json
import os

APP_DATA_FILE = "app_data.json"

# ---------------- SIDEBAR LOGO ----------------
def sidebar_logo():
    """
    Show the fallback logo at the top of the sidebar.
    """
    show_logo(None, in_sidebar=True)

# ---------------- APP DATA ----------------
def load_app_data():
    """
    Load app data from JSON file.
    If file does not exist, create default structure.
    """
    if not os.path.exists(APP_DATA_FILE):
        default_data = {"logo_url": None}
        save_app_data(default_data)
        return default_data

    try:
        with open(APP_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If JSON is corrupted, reset
        default_data = {"logo_url": None}
        save_app_data(default_data)
        return default_data

def save_app_data(data: dict):
    """
    Save app data to JSON file.
    """
    with open(APP_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
