import streamlit as st
import json
import os

DATA_FILE = "app_data.json"

# ---------------- JSON DATA HANDLING ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"logo": None, "language": "Kurdish", "products": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # If file is empty or corrupted, reset to default
        return {"logo": None, "language": "Kurdish", "products": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
